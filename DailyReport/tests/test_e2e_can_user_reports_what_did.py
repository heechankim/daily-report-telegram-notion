import asyncio

from DailyReport.tests.chat_receiver import Receiver
from DailyReport.tests.chat_messages import Messages


def get_message_from_bot(msg: str):
    print("from bot :" + msg)


def get_message_from_me(msg: str):
    print("from me :" + msg)


def test_can_user_reports_what_did(config, bot):
    receiver = Receiver(
        config=config,
        messages=Messages(
            bot_message_callback=get_message_from_bot,
            my_message_callback=get_message_from_me
        )
    )

    async def jobs():
        runners = await asyncio.gather(
            receiver.listen(),
            bot.start()
        )
        print(runners)

    asyncio.run(jobs())
