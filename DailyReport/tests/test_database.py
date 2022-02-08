import pytest
import pytest_mock
from time import sleep

from DailyReport.databases import Database
from DailyReport.utils import Left, Right


def test_database_is_user(mocker, context, db):
    database = Database()

    mocker.patch(
        "DailyReport.databases.Database.connection",
        return_value=db
    )

    result = database.is_user({
        "telegram_id": 12
    })

    assert isinstance(result, Left)
