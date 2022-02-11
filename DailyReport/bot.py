import logging
import datetime

from aiogram import Bot, Dispatcher, executor, types


logger = logging.getLogger(__name__)


class ReportingBot:

    def __init__(
            self,
            token,
            commands,
            routines
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

        #
        #
        # self.__commands = [func for func in dir(commands) if
        #                    callable(getattr(commands, func)) and not func.startswith("_")]
        # for command in self.__commands:
        #     self.dispatcher.add_handler(
        #         CommandHandler(command, getattr(commands, command), run_async=True)
        #     )
        #
        # self.__routines = [func for func in dir(routines) if
        #                    callable(getattr(routines, func)) and not func.startswith("_")]
        #
        # for routine in self.__routines:
        #     self.job_queue.run_repeating(
        #         getattr(routines, routine),
        #         interval=datetime.timedelta(hours=1),
        #         first=get_delayed_time_to_start()
        #     )
        #
        # self.dispatcher.add_error_handler(self.error_handler)

    def run(self):
        self.start()

    def start(self):
        executor.start_polling(self.dispatcher, skip_updates=True)
