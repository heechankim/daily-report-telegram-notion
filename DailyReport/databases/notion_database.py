import logging
import asyncio

from DailyReport.databases.database import Database
from DailyReport.databases.notion_apis import NotionAPIs
from DailyReport.utils.Either import Left, Right
from DailyReport.entities import User


class NotionDatabase:
    def __init__(self, db: Database):
        self.db = db
        self.log = logging.getLogger("[CLASS_notion_database]")
        # self.loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(self.loop)

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

    async def init_user_root_notion_page(self, context, log):
        log.info("2")
        result = Right(context) | \
            self.db.is_user | \
            self.db.get_user

        log.info("3")
        if isinstance(result, Left):
            return result

        user = result.context['user']

        if not user.pages['root']:
            return Left(dict(result=False, message="Notion Root page id isn't exist."))

        if not user.integration:
            return Left(dict(result=False, message="Notion Integration Token isn't exist."))

        api = NotionAPIs(user.integration)
        log.info("4")

        user.pages['daily'] = await api.init_app_page(user.pages['root'])

        log.info(result.context)

        result.context['message'] = "App is now started"

        return result

        # async def perform(db: Database, api: NotionAPIs, user: User, log: logging.Logger):
        #     daily_page_id = await api.init_app_page(user.pages['root'])
        #     user.pages['daily'] = daily_page_id
        #
        #     log.info("[perform: d_p_i] " + str(daily_page_id))
        #     log.info("[perform: User] " + str(vars(user)))
        #
        #     done(db, user, log)
        #
        # def done(db: Database, user: User, log: logging.Logger):
        #     if user.pages['daily']:
        #         db.update_user({
        #             "telegram_id": user.chat_id,
        #             "user": user
        #         })
        #
        # task = self.loop.create_task(
        #     perform(db=self.db, api=api, user=user, log=self.log)
        # )
        #
        # self.loop.run_until_complete(task)
        #
        # result.context['message'] = "App is now started"
        #
        # return result

    def report(self, context):
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

        if self.api is None:
            return Left(dict(result=False, message="Need Initialized"))

    def report_insert(self, context):
        ...

# message_len = len(str(context['root_page_id']).strip()) # 32