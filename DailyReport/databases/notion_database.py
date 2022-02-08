from DailyReport.databases.database import Database
from DailyReport.utils.Either import Left, Right

from notion_client import AsyncClient


class NotionDatabase:
    def __init__(self, db: Database):
        self.db = db

    def new_user(self, context):
        result = Right(context) | \
            self.db.is_user | \
            self.db.init_user

        return result

    def set_user_root(self, context):
        result = Right(context) | \
            self.db.is_user

    def set_user_token(self, context):
        result = Right(context) | \
            self.db.is_user | \
            self.db.set_user_integration_token

        return result

    def report(self, context):
        result = Right(context) | \
            self.db.is_user | \
            self.db.get_user | \
            self.report_insert

        return result

    def report_insert(self, context):
        ...

# message_len = len(str(context['root_page_id']).strip()) # 32