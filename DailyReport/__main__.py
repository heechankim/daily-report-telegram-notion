"""Main module."""
from dependency_injector.wiring import Provide, inject

from DailyReport import Container, ReportingBot


@inject
def main(bot: ReportingBot = Provide[Container.bot]) -> None:
    bot.run()


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
