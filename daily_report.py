# python-telegram-bot
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import JobQueue

# APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

# logger
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# env
from dotenv import dotenv_values

import datetime

# calculate run_repeating's first parameter
def get_time_delay_to_start():
    now = datetime.datetime.now()
    start = now.replace(minute=50, second=00)

    if now.minute in range(50, 60):
        start += datetime.timedelta(hours=1)

    return start - now

class App:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ENV = dotenv_values(".env")
        self.updater = Updater(token=self.ENV['TELEGRAM_BOT_TOKEN'], use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue
        self.count = 0

    def rp_command(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=self.ENV['TELEGRAM_CHAN_ID'], text="command rp testing")

    def callback_report_alarm(self, context: CallbackContext):
        self.count += 1
        context.bot.send_message(chat_id=self.ENV['TELEGRAM_CHAN_ID'],
                                 text="report alarm! [" + str(self.count) + "]\n" + datetime.datetime.now().isoformat(timespec='seconds'))

    def start(self):

        self.rp_handler = CommandHandler('rp', self.rp_command)
        self.dispatcher.add_handler(self.rp_handler)

        job_daily_report = self.job_queue.run_repeating(
            self.callback_report_alarm,
            interval=datetime.timedelta(hours=1),
            first=get_time_delay_to_start()
        )

        self.updater.start_polling()
        self.updater.idle()