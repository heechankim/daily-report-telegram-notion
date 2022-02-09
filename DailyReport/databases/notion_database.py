import logging

from DailyReport.databases.database import Database
from DailyReport.utils.Either import Left, Right


class NotionDatabase:
    def __init__(self, db: Database):
        self.db = db
        self.log = logging.getLogger("[CLASS_notion_database]")

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

    def set_user_root_notion_page(self, context):
        result = Right(context) | \
            self.db.is_user | \
            self.db.get_user

        if isinstance(result, Left):
            return result

        user = result.context['user']


    def report(self, context):
        result = Right(context) | \
            self.db.is_user | \
            self.db.get_user

        return result

    def report_insert(self, context):
        ...

# message_len = len(str(context['root_page_id']).strip()) # 32