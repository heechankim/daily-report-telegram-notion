# module
from DailyReport.utils import configuration

from telethon.sync import TelegramClient, events

import asyncio

from pprint import pprint
import sys
import logging

logger = logging.getLogger("TelegramChat")
logging.basicConfig(stream=sys.stdout,
                    format="%(levelname)-8s [%(asctime)s] [%(threadName)s_%(thread)d] %(name)s: %(message)s"
                    )


class TelegramChat:
    def __init__(
            self,
            config: dict,
            messages=None,
    ):
        logger.info("Telegram Chat init")

        self.message = messages

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

    async def listen(self):
        logger.info("Start listen ...")

        await self.client.connect()
        await self.client.run_until_disconnected()

    async def get_message_with_bot_chat(self, event):
        if event.sender_id == int(self.bot_id):
            logger.info("Receive from bot :" + event.raw_text)
        else:
            logger.info("Receive from me :" + event.raw_text)

        if "/testend" in event.raw_text:
            await self.client.disconnect()


async def main():
    client = TelegramChat(config=configuration())

    await client.listen()

    client.client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
