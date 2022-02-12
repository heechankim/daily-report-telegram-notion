import logging
import sys

from dependency_injector import containers, providers

from .bot import ReportingBot
from .commands import Commands
from .job_queue import JobQueue
from .databases import NotionDatabase, Database


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

    JobQueue = providers.Singleton(
        JobQueue,
    )

    bot = providers.Singleton(
        ReportingBot,
        token=config.telegram.bot.token,
        commands=commands,
        jobqueue=JobQueue,
    )