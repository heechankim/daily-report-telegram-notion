from DailyReport.utils.Either import Left, Right
from DailyReport.entities.User import User

from tinydb import TinyDB, where
import pathlib


FILE = pathlib.Path(__file__)
DIR = FILE.parent
DB = DIR / "db.json"


class Database:
    def __init__(self):
        self.path = DB

    def init_user(self, context):
        either = self.is_user(context)

        if isinstance(either, Right):
            return Left({"message": "이미 생성된 계정 입니다."})
        else:
            telegram_id = context['telegram_id']
            root_page_id = context['root_page_id']
            with TinyDB(self.path) as db:
                users = db.table("users")
                result = users.insert({
                    "id": telegram_id,
                    "pages": {
                        "root": root_page_id,
                        "daily": "",
                    },
                    "integration": ""
                })
                return Right({"result": result})

    def set_user_integration_token(self, context):
        either = self.is_user(context)

        if isinstance(either, Right):
            telegram_id = context['telegram_id']
            integration_token = context['integration_token']
            with TinyDB(self.path) as db:
                users = db.table("users").get(where('id') == telegram_id)
                result = users.update({
                    "integration": integration_token
                })
                return Right({"result": result})
        else:
            return Left({"message": "생성되지 않은 유저."})

    def is_user(self, context):
        with TinyDB(self.path) as db:
            telegram_id = context['telegram_id']
            result = db.table("users").get(where('id') == telegram_id)

            if result is not None:
                return Right({"result": True})
            else:
                return Left({"message": "\'/start page_id\' 로 페이지 추가 필요."})

    def get_user(self, context):
        with TinyDB(self.path) as db:
            telegram_id = context['telegram_id']
            result = db.table("users").get(where('id') == telegram_id)

            if result is not None:
                return Right({
                    "result": User(*result)
                })
            else:
                Left({"message": str(telegram_id) + "is not a user"})



