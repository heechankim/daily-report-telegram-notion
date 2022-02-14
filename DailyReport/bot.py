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
    ):
        self.bot = Bot(token=token)
        self.dispatcher = Dispatcher(self.bot)

        all_commands = [func for func in dir(commands) if
                        callable(getattr(commands, func)) and not func.startswith("_")]

        for c in all_commands:
            self.dispatcher.register_message_handler(
                getattr(commands, c),
                commands=[c]
            )

    def run(self):
        self.start()

    def start(self):
        executor.start_polling(self.dispatcher, skip_updates=True)
