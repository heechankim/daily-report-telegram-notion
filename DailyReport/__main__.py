"""Main module."""
from dependency_injector.wiring import Provide, inject

from DailyReport import Container, ReportingBot
from DailyReport import Routines


@inject
def main(
        bot: ReportingBot = Provide[Container.bot],
        routine: Routines = Provide[Container.routines],
) -> None:
    routine.run()
    bot.run()
    routine.shutdown()


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
