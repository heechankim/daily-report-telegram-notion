import pytest

from telethon import TelegramClient, events

# application
from DailyReport.utils import configuration
from DailyReport.bot import ReportingBot


@pytest.fixture
def config():
    return configuration()


@pytest.fixture
def client(config):
    _client = TelegramClient(
        config.telegram.me.name,
        config.telegram.me.api.id,
        config.telegram.me.api.hash
    )
    return _client


def test_get_config(config):
    assert config.telegram.me.name == "chan"


# def test_get_message_from_bot(config, client):
#     bot = ReportingBot(config)
#     bot.run()
#
#     @client.on(events.NewMessage(chats=config.telegram.bot.name))
#     async def _get_message_from_bot(event):
#         assert event.raw_text == "Hello World!!"
#
#     # if bot.is_idle():
#     #     client.start()
#     #     client.connect()
#     #     client.send_message(config.telegram.bot.name, "/start")
#     #     client.run_until_disconnected()


def test_is_bot_running(config):
    bot = ReportingBot(config)
    bot.run()

    assert bot.is_idle() == True
