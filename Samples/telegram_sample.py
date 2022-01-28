from dotenv import dotenv_values
CHAN = dotenv_values(".env")

# Updater
from telegram.ext import Updater
updater = Updater(token=CHAN['TOKEN'], use_context=True)

# Dispatcher
dispatcher = updater.dispatcher

# Logger
# import logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                      level=logging.INFO)

# Function
from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=CHAN['CHAT_ID'], text="I'm a bot, please talk to me!")

# CommandHandler
from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()