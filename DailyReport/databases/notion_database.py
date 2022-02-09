from DailyReport.databases.database import Database
from DailyReport.utils.Either import Left, Right

from notion_client import AsyncClient


class NotionDatabase:
    def __init__(self, db: Database):
        self.db = db

    def new_user(self, context):
        c = self.db.is_user(context)
        is_user = c.context['result']

        if is_user is True:
            return Left(dict(result=False))

        result = self.db.init_user(context)
        return result

    def set_user_info(self, context):
        result = Right(context) | \
            self.db.is_user | \
            self.db.get_user | \
            self.db.update_user

        return result

    def report(self, context):
        result = Right(context) | \
            self.db.is_user | \
            self.db.get_user

        return result

    def report_insert(self, context):
        ...

# message_len = len(str(context['root_page_id']).strip()) # 32