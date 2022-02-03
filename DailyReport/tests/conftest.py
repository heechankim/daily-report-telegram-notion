import pytest

# modules
from DailyReport.utils import configuration
from DailyReport.bot import ReportingBot


@pytest.fixture
def config():
    return configuration()


@pytest.fixture
def bot(config):
    return ReportingBot(config.telegram)


