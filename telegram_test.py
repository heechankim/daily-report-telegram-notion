
# from telegram.ext import Updater
# updater = Updater(token='TOKEN', use_context=True)
#
# dispatcher = updater.dispatcher
#
# import logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                      level=logging.INFO)
#
# from telegram import Update
# from telegram.ext import CallbackContext
#
# def start(update: Update, context: CallbackContext):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
#
# from telegram.ext import CommandHandler
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)
#
# updater.start_polling()
#
# from telegram.ext import MessageHandler, Filters
#
# def echo(update: Update, context: CallbackContext):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
#
# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
# dispatcher.add_handler(echo_handler)
#
# updater.stop()

import telegram
bot = telegram.Bot(token=token)
updates = bot.getUpdates()
chat_id = updates[-1].message.chat_id

bot.sendMessage(chat_id=chat_id, text="hello!")

for update in updates:
    print(update.message)