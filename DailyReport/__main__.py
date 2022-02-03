"""Main module."""

from DailyReport.bot import ReportingBot
from DailyReport.utils import configuration


def main():
    config = configuration()
    bot = ReportingBot(config.telegram)

    bot.start()


if __name__ == "__main__":
    main()
