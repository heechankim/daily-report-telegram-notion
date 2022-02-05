from telegram.ext import CallbackContext
from telegram import Update


class Commands:
    def __init__(
            self,
            chat_id: int
    ):
        self.chat_id = chat_id

    def start(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=self.chat_id,
            text="Testing Start Command."
        )

    def rp(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=self.chat_id,
            text="Testing report Command."
        )

    def todo(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=self.chat_id,
            text="Testing todo Command."
        )