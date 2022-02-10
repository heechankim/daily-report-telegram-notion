import logging
import traceback
import html, json

from DailyReport.utils.utils import get_delayed_time_to_start

from telegram import Update, ParseMode
from telegram.ext.dispatcher import Dispatcher
from telegram.bot import Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext
)

import datetime

DEVELOPER_CHAT_ID = 2084891827

class ReportingBot:

    def __init__(
            self,
            token,
            bot_id,
            my_id,
            commands,
            routines
    ):
        self.logger = logging.getLogger("[ReportingBot]")
        self.bot = Bot(token=token)
        self.id = bot_id
        self.my_id = my_id

        self.updater = Updater(bot=self.bot)
        self.dispatcher: Dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue

        self.__commands = [func for func in dir(commands) if
                           callable(getattr(commands, func)) and not func.startswith("_")]
        for command in self.__commands:
            self.dispatcher.add_handler(
                CommandHandler(command, getattr(commands, command), run_async=True)
            )

        self.__routines = [func for func in dir(routines) if
                           callable(getattr(routines, func)) and not func.startswith("_")]

        for routine in self.__routines:
            self.job_queue.run_repeating(
                getattr(routines, routine),
                interval=datetime.timedelta(hours=1),
                first=get_delayed_time_to_start()
            )

        self.dispatcher.add_error_handler(self.error_handler)

    def error_handler(self, update: object, context: CallbackContext) -> None:
        """Log the error and send a telegram message to notify the developer."""
        # Log the error before we do anything else, so we can see it even if something breaks.
        self.logger.error(msg="Exception while handling an update:", exc_info=context.error)

        # traceback.format_exception returns the usual python message about an exception, but as a
        # list of strings rather than a single string, so we have to join them together.
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = ''.join(tb_list)

        # Build the message with some markup and additional information about what happened.
        # You might need to add some logic to deal with messages longer than the 4096 character limit.
        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        message = (
            f'An exception was raised while handling an update\n'
            f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
            '</pre>\n\n'
            f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
            f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
            f'<pre>{html.escape(tb_string)}</pre>'
        )

        # Finally, send the message
        context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)

    def run(self):
        self.start()

    def start(self):
        self.updater.start_polling()
        self.updater.idle()
