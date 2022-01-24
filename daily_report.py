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

    def callback_alarm(self, context: CallbackContext):
        context.bot.send_message(chat_id=context.job.context, text='BEEP')

    def callback_timer(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Setting a timer for 1 minute!')

        context.job_queue.run_once(self.callback_alarm, 60, context=update.message.chat_id)

    def start(self):

        self.rp_handler = CommandHandler('rp', self.rp_command)
        self.dispatcher.add_handler(self.rp_handler)

        self.timer_handler = CommandHandler('timer', self.callback_timer)
        self.dispatcher.add_handler(self.timer_handler)

        self.updater.start_polling()
        self.updater.idle()



    def __del__(self):
        self.updater.stop()
        print("########## shutdown app ##########")
