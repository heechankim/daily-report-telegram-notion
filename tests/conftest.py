import pytest

# 3rd-party
from telethon.sync import TelegramClient, events

# application
from DailyReport.utils import configuration
from DailyReport.bot import ReportingBot

from .telegram_mine import TelegramMine
from .chat_queue import ChatQueue


@pytest.fixture(scope="session")
def messages():
    return ChatQueue()


@pytest.fixture(scope="session")
def config():
    return configuration()


@pytest.fixture(scope="session")
def chat(config, messages):
    chat = TelegramMine(config)

    return chat


@pytest.fixture
def telegram_bot(config):
    return ReportingBot(config.telegram)


