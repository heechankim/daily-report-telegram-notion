import logging
import asyncio
from aiogram import Bot, exceptions
from contextlib import asynccontextmanager

from DailyReport.databases import Database

logger = logging.getLogger("[Routines]")


class Loop:
    def __init__(self):
        self.loop = None

    def __enter__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        return self.loop

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.loop.close()

    def __lt__(self, other):
        self.loop.run_until_complete(other)


class Routines:
    def __init__(
            self,
            bot: Bot,
    ):
        self.bot = bot

    def reporting_alarm(self) -> None:

        async def perform():
            user_id = 2084891827

            text = "Report:"

            try:
                await asyncio.sleep(1)

            except exceptions.RetryAfter as e:
                logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
                await asyncio.sleep(e.timeout)
                return await perform()  # Recursive call

            except exceptions.TelegramAPIError as e:
                logger.exception(f"Target [ID:{user_id}]: failed")

            else:
                logger.exception("reporting alarm method done.")

        asyncio.run(perform())
