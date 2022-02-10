import pytest
import pytest_mock

from DailyReport.databases.notion_apis import (
Response,
NotionAPIs
)
from DailyReport.entities import RichText

from DailyReport.utils import configuration
config = configuration("./config.yml").notion
#
#
# def test_init_sub_create_daily_page(mocker):
#     mocker.patch
