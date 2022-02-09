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
            return Right(dict(context, result=result, message="Success init user info."))
        else:
            return Left(dict(result=False, message="Failed, while creating user."))

    def is_user(self, context):
        telegram_id = context['telegram_id']

        row = self.db.table("users").get(where('chat_id') == telegram_id)

        if row is not None:
            return Right(dict(context, result=True, message="User is exist."))
        else:
            return Left(dict(result=False, message="User is not exist."))

    def get_user(self, context):
        telegram_id = context['telegram_id']

        row = self.db.table("users").get(where('chat_id') == telegram_id)

        if row is not None:
            return Right(dict(context, user=User(**row),
                              message="Success get user data."))
        else:
            return Left(dict(result=None, message="User is not exist."))

    def update_user(self, context):
        telegram_id = context['telegram_id']

        message = ""

        try:
            if context['root'] is not None:
                _root = str(context['root'])
                context['user'].pages['root'] = _root.strip()
                message += "Root Page "
        except KeyError as k:
            ...

        try:
            if context['daily'] is not None:
                _daily = str(context['daily'])
                context['user'].pages['daily'] = _daily.strip()
                message += "Daily Page "
        except KeyError as k:
            ...

        try:
            if context['integration'] is not None:
                _integration = str(context['integration'])
                context['user'].integration = _integration.strip()
                message += "Notion Integration "

        except KeyError as k:
            ...

        table = self.db.table("users")

        result = table.update(
            vars(context['user']),
            where('chat_id') == telegram_id
        )

        if result is not None:
            return Right(dict(context, result=result,
                              message="Success update user {0}info.".format(
                                  message
                              )))
        else:
            return Left(dict(result=False, message="Failed, while updating information."))