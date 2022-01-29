
from telegram.bot import Bot


class ReportingBot:

    def __init__(
            self,
            config: dict,
    ):
        self.bot = Bot(token=config.bot.token)
        self.id = config.bot.id
        self.me_id = config.me.id

    def send_message(self, message: str):
        self.bot.send_message(
            self.me_id,
            message
        )