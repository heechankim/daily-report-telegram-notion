"""Main module."""

import yaml
import logging, sys
from pprint import pprint

# application
from .utils import configuration
from .bot import ReportingBot


def main():
    config = configuration()
    logging.basicConfig(
        stream=sys.stdout,
        level=config.log.level,
        format=config.log.format,
    )

    bot = ReportingBot(config)
    bot.run()


if __name__ == "__main__":
    main()
