import logging
import datetime

from DailyReport.databases.database import Database
from DailyReport.databases.notion_apis import NotionAPIs
from DailyReport.utils import Left, Right
from DailyReport.entities import User

logger = logging.getLogger("[NotionDatabase]")


class NotionDatabase:
    def __init__(self, db: Database):
        self.db = db

    def new_user(self, context):
        exist_then_right = self.db.is_user(context)

        if isinstance(exist_then_right, Right):
            return exist_then_right

        result = self.db.init_user(context)
        return result

    def set_user_info(self, context):
        result = Right(context) | \
            self.db.is_user | \
            self.db.get_user | \
            self.db.update_user

        return result

    async def init_user_root_notion_page(self, context):
        result = Right(context) | \
            self.db.is_user | \
            self.db.get_user

        if isinstance(result, Left):
            return result

        user = result.context['user']

        if not user.pages['root']:
            return Left(dict(result=False, message="Notion Root page id isn't exist."))

        if not user.integration:
            return Left(dict(result=False, message="Notion Integration Token isn't exist."))

        async with NotionAPIs(token=user.integration) as api:
            user.pages['daily'] = await api.init_app(user.pages['root'])

            if user.pages['daily']:
                result = result | self.db.update_user

            result.context['message'] = "App is now started"

        return result

    async def report(self, context):
        result = Right(context) | \
            self.db.is_user | \
            self.db.get_user

        if isinstance(result, Left):
            return result

        user = result.context['user']

        if not user.pages['daily']:
            return Left(dict(result=False, message="Notion Daily page id isn't exist."))

        if not user.integration:
            return Left(dict(result=False, message="Notion Integration Token isn't exist."))

        async with NotionAPIs(token=user.integration) as api:

            # TODO: 스케줄러로 생성하기.
            res = await api.create_today_report(user.pages['daily'])
            date = datetime.date.today().isoformat()
            hour = context['datetime'].now().astimezone().now().hour

            res = await api.is_today_exist(user.pages['daily'])

            if res.result:
                res = await api.update_report_prop(
                    user.pages['daily'],
                    hour,
                    context['message']
                )

        result.context['message'] = "Done."

        return result
