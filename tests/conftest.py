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

    db_.table("users").insert({
        "chat_id": 9999,
        "pages": {
            "root": "",
            "daily": ""},
        "integration": ""
    })

    return db_


# python-telegram-bot.Update
@dataclasses.dataclass
class FromUser:
    id: int


@dataclasses.dataclass
class Message:
    text: str
    date: datetime.datetime
    from_user: FromUser


@dataclasses.dataclass
class Update:
    message: Message


@pytest.fixture
def update():
    return Update(
        message=Message(
            text="",
            date=None,
            from_user=FromUser(
                id=0
            )
        )
    )


# python-telegram-bot.Context
class Bot:
    def __init__(self):
        self.chat_id: int
        self.text: str

    def send_message(
            self,
            chat_id,
            text
    ):
        self.chat_id = chat_id
        self.text = text


@dataclasses.dataclass
class Context:
    bot: Bot


@pytest.fixture
def context():
    return Context(bot=Bot())


