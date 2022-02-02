from DailyReport.utils import configuration

from telegram.bot import Bot
from telegram import (
Update,
)
from telegram.ext import (
Updater,
CallbackContext,
CommandHandler
)

from pprint import pprint


class ReportingBot:

    def __init__(
            self,
            config: dict,
    ):
        self.bot = Bot(token=config.bot.token)
        self.id = config.bot.id
        self.me_id = config.me.id

        self.updater = Updater(bot=self.bot)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue

    def send_message(self, message: str):
        try:
            self.bot.send_message(self.me_id, message)

            return message

        except Exception as e:
            raise

    def start_command(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=self.me_id,
            text="testing start command",
        )

    def start(self):

        self.dispatcher.add_handler(
            CommandHandler("start", self.start_command)
        )
        self.updater.start_polling()
        self.updater.idle()



if __name__ == "__main__":
    config = configuration()
    bot = ReportingBot(config.telegram)

    bot.start()

