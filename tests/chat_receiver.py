# module
from DailyReport.utils import configuration
from chat_messages import Messages


from telethon.sync import TelegramClient, events

import asyncio
import sys
import logging
import threading


class Receiver:
    def __init__(
            self,
            config: dict,
            messages: Messages = None,
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
            self.message.bot_said(event.raw_text)

        else:
            self.logger.info("Receive from me :" + event.raw_text)
            self.message.bot_said(event.raw_text)

        if "/testend" in event.raw_text:
            await self.client.disconnect()



def get_message(msg: str):
    print("        #####from_bot#####")
    print("                " + msg)
    print("        #####from_bot#####")


async def main():
    msg = Messages(
        bot_message_callback=get_message
    )
    client = Receiver(
        config=configuration(),
        messages=msg,
    )

    await client.listen()

    print("end of the main function")
    print(threading.active_count())


if __name__ == "__main__":
    asyncio.run(main())
