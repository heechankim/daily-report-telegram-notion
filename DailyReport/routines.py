from telegram.ext import CallbackContext

import datetime


class Routines:
    def __init__(
            self,
            chat_id
    ):
        self.chat_id = chat_id

    def report_alarm(self, context: CallbackContext):
        context.bot.send_message(
            chat_id=self.chat_id,
            text="report alarm" + datetime.datetime.now().isoformat(timespec='seconds')
        )
