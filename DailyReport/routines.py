import logging
import asyncio
from aiogram import Bot, exceptions
import datetime

from DailyReport.job_queue import JobQueue, Job
from DailyReport.utils import get_report_time_50_min

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
            token,
            jobqueue: JobQueue,
    ):
        self.bot = Bot(token=token)
        self.sch = jobqueue

        self.sch.run_repeating(
            self.reporting_alarm,
            interval=datetime.timedelta(hours=1),
            first=get_report_time_50_min(),
            # first=datetime.timedelta(seconds=5),
        )

    def run(self):
        self.start()

    def start(self):
        self.sch.start()

    def shutdown(self):
        self.sch.stop()

    def reporting_alarm(self) -> None:

        async def perform():
            user_id = 2084891827

            text = "Report:"

            try:
                await self.bot.send_message(user_id, text)

            except exceptions.RetryAfter as e:
                logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
                await asyncio.sleep(e.timeout)
                return await perform()  # Recursive call

            except exceptions.TelegramAPIError as e:
                logger.exception(f"Target [ID:{user_id}]: failed")

            finally:
                logger.info("reporting alarm method done.")

        asyncio.run(perform())
