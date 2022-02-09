import pytest
import pytest_mock
import logging
from time import sleep

from DailyReport.databases import Database
from DailyReport.utils import Left, Right
from DailyReport.entities import User


log = logging.getLogger("[TEST_database]")


@pytest.fixture
def database(mocker, db):
    mocker.patch(
        "DailyReport.databases.Database.connection",
        return_value=db
    )

    database = Database()

    return database


def test_init_user(database):
    result = database.init_user({
        "telegram_id": 12
    })

    assert isinstance(result, Right)
    assert result.context['result'] == 1


def test_is_exist_user(database):
    telegram_id = 12

    database.init_user({
        "telegram_id": telegram_id
    })

    result = database.is_user({
        "telegram_id": telegram_id
    })

    assert isinstance(result, Right)
    assert result.context['result'] is True


def test_is_non_exist_user(database):
    telegram_id = 12

    result = database.is_user({
        "telegram_id": telegram_id
    })

    assert isinstance(result, Left)
    assert result.context['result'] is False


def test_get_exist_user(database):
    telegram_id = 12

    database.init_user({
        "telegram_id": telegram_id
    })

    result = database.get_user({
        "telegram_id": telegram_id
    })

    assert isinstance(result, Right)
    assert isinstance(result.context['user'], User)
    assert result.context['user'].chat_id == telegram_id


def test_get_non_exist_user(database):
    telegram_id = 12

    result = database.get_user({
        "telegram_id": telegram_id
    })

    assert isinstance(result, Left)
    assert result.context['result'] is None


def test_update_user(database):
    telegram_id = 12
    updated_root_page = "test_root_page"
    updated_daily_page = "test_daily_page"
    updated_integration = "test_integration"

    database.init_user({
        "telegram_id": telegram_id
    })

    u = database.get_user({
        "telegram_id": telegram_id
    })

    u.context['user'].pages['root'] = updated_root_page

    result = database.update_user(dict(
        u.context,
        root=updated_root_page,
        daily=updated_daily_page,
        integration=updated_integration
    ))

    assert isinstance(result, Right)
    assert len(result.context['result']) is 1

    u = database.get_user({
        "telegram_id": telegram_id
    })

    assert u.context['user'].pages['root'] is updated_root_page
