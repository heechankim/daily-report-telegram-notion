import pytest
import dataclasses
import datetime


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
    return Context()


