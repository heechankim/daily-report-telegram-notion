from telethon.sync import TelegramClient, events

from .chat_queue import ChatQueue

import logging


class TelegramMine:
    def __init__(
            self,
            config: dict
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Telegram Mine init")
        self.client = TelegramClient(
            config.telegram.me.name,
            config.telegram.me.api.id,
            config.telegram.me.api.hash
        )
        self.bot_name = config.telegram.bot.name
        self.bot_id = config.telegram.bot.id

        self.client.add_event_handler(
            self.get_message_with_bot_chat,
            events.NewMessage(chats=self.bot_name)
        )

    def listen(self):
        self.logger.info("Start connect")

        self.client.start()
        self.client.connect()
        self.client.run_until_disconnected()

    async def get_message_with_bot_chat(self, event):
        assert 0
        self.logger.info("Receive New Messages: " + event.raw_text)
        if event.sender_id == int(self.bot_id):
            print("bot : " + event.raw_text)
            if "TEST_END" in event.raw_text:
                await self.client.disconnect()
        else:
            print("me: " + event.raw_text)
