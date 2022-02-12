import logging
import asyncio
import datetime

from aiogram import Bot, Dispatcher, executor, exceptions

from DailyReport.utils import get_report_time_50_min
from DailyReport.routines import Routines


logger = logging.getLogger(__name__)


class ReportingBot:

    def __init__(
            self,
            token,
            commands,
            jobqueue
    ):
        self.bot = Bot(token=token)
        self.dispatcher = Dispatcher(self.bot)
        self.scheduler = jobqueue

        self.routines = Routines(self.bot)

        all_commands = [func for func in dir(commands) if
                        callable(getattr(commands, func)) and not func.startswith("_")]

        for c in all_commands:
            self.dispatcher.register_message_handler(
                getattr(commands, c),
                commands=[c]
            )

        self.scheduler.run_repeating(
            self.routines.reporting_alarm,
            interval=datetime.timedelta(hours=1),
            # first=get_report_time_50_min(),
            first=datetime.timedelta(seconds=5),
        )

    def run(self):
        self.scheduler.start()
        self.start()
        self.scheduler.stop()

    def start(self):
        executor.start_polling(self.dispatcher, skip_updates=True)
