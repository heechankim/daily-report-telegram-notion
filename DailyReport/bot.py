"""python-telegram-bot wrap module."""
import asyncio
import logging
import threading
import os, signal

from telegram.ext import(
Updater,
CallbackContext,
CommandHandler,
JobQueue
)

# application
from .utils import configuration


class ReportingBot:
    def __init__(
            self,
            _config: dict
    ):
        self.config = _config
        self.updater = Updater(
            token=self.config.telegram.bot.token,
            use_context=True
        )
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue
        self._logger = logging.getLogger(self.__class__.__name__)

    def run(self):
        self.start()

    def start(self):
        self.dispatcher.add_handler(
            CommandHandler("start", self.start_command)
        )
        self.job_queue.run_once(
            self.stop_job,
            3
        )
        self.updater.start_polling()
        self.updater.idle()

    def start_command(self, context: CallbackContext):
        context.bot.send_message(
            chat_id=self.config.telegram.me.id,
            text="Hello World!!"
        )

    def stop_job(self, update):
        threading.Thread(target=self.shutdown_bot).start
        os.kill(os.getpid(), signal.SIGINT)

    def shutdown_bot(self):
        self.updater.stop()
        self.updater.is_idle = False
