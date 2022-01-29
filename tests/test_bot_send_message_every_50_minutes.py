import asyncio
import logging


def test_can_bot_send_a_message(telegram_bot, chat, messages):
    logger = logging.getLogger("test_can_bot_send_a_message")

    asyncio.ensure_future(chat.listen())

    telegram_bot.send_message("Hello World!")
    logger.info("Send Hello World!")

    telegram_bot.send_message("TEST_END")
    logger.info("Send TEST_END")





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


