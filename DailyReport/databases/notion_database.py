from DailyReport.databases.database import Database
from DailyReport.utils.Either import Left, Right

from notion_client import AsyncClient


class NotionDatabase:
    def __init__(self, db: Database):
        self.db = db

    def new_user(self, context):
        message_len = len(str(context['root_page_id']).strip())
        # if message_len is not 32:
        #     return Left({"message": "올바른 페이지 id 입력"})
        # elif:
        #     return self.db.init_user(context)

        if message_len is 32:
            return self.db.init_user(context)
        elif message_len is 0:
            return Left({"message":
                         "/start page_id\n" +
                         "/setToken token_id\n" +
                         "/rp 한 시간 동안 한일\n"})
        else:
            return Left({"message": "올바른 페이지 id 입력"})

    def set_user_token(self, context):
        either = self.db.is_user(context) | \
            self.db.set_user_integration_token(context)

        return either

    def report(self, context):
        either = self.db.is_user(context) | \
            self.db.get_user(context)

        return either
