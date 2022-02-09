import pytest
import dataclasses
import datetime
import pathlib
import logging

from tinydb.storages import MemoryStorage
from tinydb import TinyDB


FILE = pathlib.Path(__file__)
DIR = FILE.parent
DB_URL = DIR / "db.json"

log = logging.getLogger("[test_database]")


# tinyDB stub
@pytest.fixture
def db():
    db_ = TinyDB(storage=MemoryStorage)
    # db_ = TinyDB(DB_URL)
    db_.drop_tables()
    return db_


# python-telegram-bot.Update
@dataclasses.dataclass
class FromUserStub:
    id: int


@dataclasses.dataclass
class MessageStub:
    text: str
    date: datetime.datetime
    from_user: FromUserStub


@dataclasses.dataclass
class UpdateStub:
    message: MessageStub


# python-telegram-bot.Context
class Bot:
    @staticmethod
    def send_message(
            self,
            chat_id,
            text
    ):
        return(dict(
            chat_id=chat_id,
            text=text
        ))


@dataclasses.dataclass
class Context:
    bot: Bot


@pytest.fixture
def context():
    return Context(bot=Bot())


