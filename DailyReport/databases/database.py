import logging
import pathlib

from tinydb import TinyDB, where

from DailyReport.utils import Left, Right
from DailyReport.entities import User


FILE = pathlib.Path(__file__)
DIR = FILE.parent
DB_URL = DIR / "db.json"


class Database:
    def __init__(
            self,
            db: TinyDB = None
    ):
        self.log = logging.getLogger("[CLASS_Database]")

        if db is None:
            self.db = self.connection()

    def __del__(self):
        self.db.close()

    def connection(self):
        conn = TinyDB(DB_URL)
        return conn

    def init_user(self, context):
        telegram_id = context['telegram_id']
        user = User(chat_id=telegram_id)

        table = self.db.table("users")

        result = table.insert(
            vars(user)
        )

        if result is not None:
            return Right(dict(context, result=result))
        else:
            return Left(dict(context, result=False))

    def set_user_integration_token(self, context):
        telegram_id = context['telegram_id']
        integration_token = context['integration_token']

        row = self.db.table("users").get(where('id') == telegram_id)

        result = row.update({
            "integration": integration_token
        })

        if result is not None:
            return Right(dict(context, result="토큰 입력 성공."))
        else:
            return Left({"message": "error occurs in set_user_integration_token"})

    def is_user(self, context):
        telegram_id = context['telegram_id']

        row = self.db.table("users").get(where('chat_id') == telegram_id)

        if row is not None:
            return Right(dict(context, result=True))
        else:
            return Left(dict(context, result=False))

    def get_user(self, context):
        telegram_id = context['telegram_id']

        row = self.db.table("users").get(where('chat_id') == telegram_id)

        if row is not None:
            return Right(dict(context, user=User(**row)))
        else:
            return Left(dict(context, result=None))

    def update_user(self, context):
        telegram_id = context['telegram_id']

        try:
            if context['root'] is not None:
                _root = context['root']
                context['user'].pages['root'] = _root

            if context['daily'] is not None:
                _daily = context['daily']
                context['user'].pages['daily'] = _daily

            if context['integration'] is not None:
                _integration = context['integration']
                context['user'].integration = _integration

        except KeyError as k:
            ...

        table = self.db.table("users")

        result = table.update(
            vars(context['user']),
            where('chat_id') == telegram_id
        )

        if result is not None:
            return Right(dict(context, result=result))
        else:
            return Left(dict(context, result=False))