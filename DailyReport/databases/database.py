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
        with TinyDB(self.path) as db:
            telegram_id = context['telegram_id']

            users = db.table("users")
            result = users.insert({
                "id": telegram_id,
                "pages": {
                    "root": "",
                    "daily": "",
                },
                "integration": ""
            })

            if result is not None:
                return Right(dict(context, result="신규 유저 생성 완료"))
            else:
                return Left({"message": "error occurs in init_user"})

    def set_user_integration_token(self, context):
        with TinyDB(self.path) as db:
            telegram_id = context['telegram_id']
            integration_token = context['integration_token']

            users = db.table("users").get(where('id') == telegram_id)
            result = users.update({
                "integration": integration_token
            })

            if result is not None:
                return Right(dict(context, result="토큰 입력 성공."))
            else:
                return Left({"message": "error occurs in set_user_integration_token"})

    def is_user(self, context):
        with TinyDB(self.path) as db:
            telegram_id = context['telegram_id']

            result = db.table("users").get(where('chat_id') == telegram_id)

            if result is not None:
                return Right(dict(context, result=True))
            else:
                return Right(dict(context, result=False))

    def get_user(self, context):
        with TinyDB(self.path) as db:
            telegram_id = context['telegram_id']

            result = db.table("users").get(where('chat_id') == telegram_id)

            if result is not None:
                return Right(dict(context, result=User(**result)))
            else:
                Left({"message": str(telegram_id) + "is not a user"})



