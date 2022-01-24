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

from pytz import timezone
import time
import datetime


class App:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ENV = dotenv_values(".env")
        self.updater = Updater(token=self.ENV['TELEGRAM_BOT_TOKEN'], use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue

    def rp_command(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=self.ENV['TELEGRAM_CHAN_ID'], text="command rp testing")

    def callback_minute(self, context: CallbackContext):
        context.bot.send_message(chat_id=self.ENV['TELEGRAM_CHAN_ID'],
                                 text="One message every minute\n" + time.strftime('%c', time.localtime(time.time())))

    def start(self):

        self.rp_handler = CommandHandler('rp', self.rp_command)
        self.dispatcher.add_handler(self.rp_handler)

        job_minute = self.job_queue.run_repeating(self.callback_minute, interval=60, first=10)

        self.updater.start_polling()
        self.updater.idle()



    def __del__(self):
        self.updater.stop()
        print("########## shutdown app ##########")
