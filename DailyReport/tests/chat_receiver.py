# module
from DailyReport.utils import configuration
from DailyReport.tests.chat_messages import Messages


from telethon.sync import TelegramClient, events

import asyncio
import sys
import logging
import threading
from pprint import pprint


class Receiver:
    def __init__(
            self,
            config: dict,
            messages,
    ):
        logging.basicConfig(stream=sys.stdout,
                            format="%(levelname)-8s [%(asctime)s] [%(threadName)s_%(thread)d] %(name)s: %(message)s"
                            )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.logger.info("Telegram Chat init")

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
        await self.client.connect()
        await self.client.run_until_disconnected()

    async def get_message_with_bot_chat(self, event):
        if event.sender_id == int(self.bot_id):
            self.logger.info("Receive from bot :" + event.raw_text)
            self.message.received(event.raw_text)

        else:
            self.logger.info("Receive from me :" + event.raw_text)
            self.message.received(event.raw_text)

        if "/testend" in event.raw_text:
            await self.shutdown()

    async def shutdown(self):
        await self.client.disconnect()
        self.message.stop()


def get_message(msg: str):
    print("        #####new message#####")
    print("                " + msg)
    print("        #####new message#####")



async def main():
    config = configuration()
    pprint(config)
    client = Receiver(
        config=config,
        messages=Messages(
            callback=get_message
        ),
    )

    await client.listen()

    print("end of the main function")
    print(threading.active_count())


if __name__ == "__main__":
    asyncio.run(main())
