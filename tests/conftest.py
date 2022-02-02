import pytest

# 3rd-party
from telethon.sync import TelegramClient, events

# application
from DailyReport.utils import configuration
from DailyReport.bot import ReportingBot

from .telegram_chat import TelegramChat


@pytest.fixture(scope="session")
def config():
    return configuration()


@pytest.fixture
def chat(config):
    chat = TelegramChat(config, None)

    return chat


@pytest.fixture
def telegram_bot(config):
    return ReportingBot(config.telegram)


