from DailyReport.utils import get_delayed_time_to_start

from telegram.bot import Bot
from telegram.ext import (
    Updater,
    CommandHandler
)

import datetime


class ReportingBot:

    def __init__(
            self,
            token,
            bot_id,
            my_id,
            commands,
            routines
    ):
        self.bot = Bot(token=token)
        self.id = bot_id
        self.my_id = my_id

        self.updater = Updater(bot=self.bot, workers=1)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue

        self.__commands = [func for func in dir(commands) if
                           callable(getattr(commands, func)) and not func.startswith("_")]
        for command in self.__commands:
            self.dispatcher.add_handler(
                CommandHandler(command, getattr(commands, command))
            )

        self.__routines = [func for func in dir(routines) if
                           callable(getattr(routines, func)) and not func.startswith("_")]

        for routine in self.__routines:
            self.job_queue.run_repeating(
                getattr(routines, routine),
                interval=datetime.timedelta(hours=1),
                first=get_delayed_time_to_start()
            )

    def run(self):
        self.start()

    def start(self):
        self.updater.start_polling()
        self.updater.idle()


# if __name__ == "__main__":
#     config = configuration()
#     bot = ReportingBot(config)
#
#     bot.start()
#
