import pytest
import logging

from DailyReport.databases import NotionDatabase, Database
from DailyReport.utils import Left, Right
from DailyReport.entities import User

log = logging.getLogger("[TEST_notion_database]")


@pytest.fixture
def database(mocker, db):
    mocker.patch(
        "DailyReport.databases.Database.connection",
        return_value=db
    )

    database = Database()

    return database


@pytest.fixture
def notion(database):

    n = NotionDatabase(database)

    return n


def test_new_user(notion):
    result = notion.new_user({
        "telegram_id": 12
    })

    assert isinstance(result, Right)



def test_call_new_user_twice(notion):
    result = notion.new_user({
        "telegram_id": 12
    })

    assert isinstance(result, Right)

    result = notion.new_user({
        "telegram_id": 12
    })

    assert isinstance(result, Right)
    assert result.context['message'] == "User is exist."


def test_set_user_info(notion):
    telegram_id = 12

    updated_root_page = "test_update_root_page"

    notion.new_user({
        "telegram_id": telegram_id
    })

    result = notion.set_user_info({
        "telegram_id": telegram_id,
        "root": updated_root_page
    })

    assert isinstance(result, Right)
