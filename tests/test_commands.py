import pytest
import logging

from DailyReport.commands import Commands
from DailyReport.databases import NotionDatabase, Database
from DailyReport.utils.Either import Either, Left, Right


log = logging.getLogger("[TEST_commands]")


@pytest.fixture
def database(mocker, db):
    mocker.patch(
        "DailyReport.databases.Database.connection",
        return_value=db
    )

    return Database()


@pytest.fixture
def notion(database):
    return NotionDatabase(database)


@pytest.fixture
def commands(notion):
    return Commands(notion=notion)


def test_start_command(commands, update, context):
    telegram_id = 12
    update.message.from_user.id = telegram_id

    commands.start(update, context)

    assert context.bot.chat_id == telegram_id


def test_set_root_command(commands, database, update, context):
    telegram_id = 9999
    raw_msg = "Test_Root_Page_ID"
    command = "/setRoot"
    update.message.from_user.id = telegram_id
    update.message.text = command + " " + raw_msg

    commands.setRoot(update, context)
    assert context.bot.chat_id == telegram_id

    user = database.get_user({"telegram_id": telegram_id}).context['user']
    assert user.pages['root'] == raw_msg

def test_set_notion_command(commands, database, update, context):
    telegram_id = 9999
    raw_msg = "Test_Integration_Token"
    command = "/setNotion"
    update.message.from_user.id = telegram_id
    update.message.text = command + " " + raw_msg

    commands.setNotion(update, context)
    assert context.bot.chat_id == telegram_id

    user = database.get_user({"telegram_id": telegram_id}).context['user']
    assert user.integration == raw_msg
    log.info(vars(user))

