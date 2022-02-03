import pytest
import logging
import sys
logging.basicConfig(stream=sys.stdout,
                    format="%(levelname)-8s [%(asctime)s] [%(threadName)s_%(thread)d] %(name)s: %(message)s"
                    )
logger = logging.getLogger(__name__)


# @pytest.mark.asyncio
# async def test_b(config, chat, messages):
#     await chat.listen()
#
#     logger.info(messages.bot.get_nowait())


def test_can_bot_send_a_message(telegram_bot):
    message = "this is a test message"

    result = telegram_bot.send_message(message)

    assert result == message




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


