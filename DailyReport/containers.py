import logging
import sys

from dependency_injector import containers, providers

from .bot import ReportingBot
from .commands import Commands
from .routines import Routines
from .databases.database import Database
from .databases.notion_database import NotionDatabase


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    logging = providers.Resource(
        logging.basicConfig,
        stream=sys.stdout,
        level=config.log.level,
        format=config.log.thread_format,
    )

    db = providers.Singleton(
        Database
    )

    notion_connection = providers.Singleton(
        NotionDatabase,
        db,
    )

    commands = providers.Singleton(
        Commands,
        notion=notion_connection,
    )

    routines = providers.Singleton(
        Routines,
        chat_id=config.telegram.my.id,
    )

    bot = providers.Singleton(
        ReportingBot,
        token=config.telegram.bot.token,
        bot_id=config.telegram.bot.id,
        my_id=config.telegram.my.id,
        commands=commands,
        routines=routines,
    )