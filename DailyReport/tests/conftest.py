import pytest
import dataclasses
import datetime

from tinydb.storages import MemoryStorage
from tinydb import TinyDB


# tinyDB stub
@pytest.fixture
def db():
    db_ = TinyDB(storage=MemoryStorage)
    db_.drop_tables()
    db_.insert_multiple({'int': 1, 'char': c} for c in 'abc')
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


