import pytest

from DailyReport.commands import Commands
from DailyReport.databases import NotionDatabase, Database


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

