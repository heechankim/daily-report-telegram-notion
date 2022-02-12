import logging
import datetime
import time
import tzlocal
import pytz
from typing import (
Callable,
Dict,
Any,
cast,
Tuple,
overload,
Union,
Optional
)

from aiogram import Bot

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.job import Job as APSJob

logger = logging.getLogger("[JobQueue]")


class Job:
    def __init__(
            self,
            callback: Callable[['Bot'], None],
            context: dict = None,
            name: str = None,
            # job_queue: JobQueue = None,
            job: APSJob = None,
    ):
        self.callback = callback
        self.context = context
        self.name = name or callback.__name__
        # self.job_queue = job_queue

        self._removed = False
        self._enabled = False

        self.job = cast(APSJob, job)

    def remove(self) -> None:
        self.job.remove()
        self._removed = True


class JobQueue:
    def __init__(self):
        self.local = tzlocal.get_localzone()._key
        self.sch = BackgroundScheduler(timezone=self.local)

    def start(self) -> None:
        if not self.sch.running:
            self.sch.start()
            logger.info("APScheduler is now running")

    def stop(self) -> None:
        if self.sch.running:
            self.sch.shutdown()
            logger.info("APScheduler has been shutdown.")

    def jobs(self) -> Tuple['Job', ...]:
        ...

    def get_jobs_by_name(self, name: str) -> Tuple['Job', ...]:
        ...

    def _tz_now(self) -> datetime.datetime:
        return datetime.datetime.now(self.sch.timezone)

    @overload
    def parse_time_input(self, time: None, shift_day: bool = False) -> None:
        ...

    @overload
    def parse_time_input(
            self,
            time: Union[float, int, datetime.timedelta, datetime.datetime, datetime.time],
            shift_day: bool = False,
    ) -> datetime.datetime:
        ...

    def parse_time_input(
            self,
            time: Union[float, int, datetime.timedelta, datetime.datetime, datetime.time, None],
            shift_day: bool = False,
    ) -> Optional[datetime.datetime]:
        if time is None:
            return None
        if isinstance(time, (int, float)):
            return self._tz_now() + datetime.timedelta(seconds=time)
        if isinstance(time, datetime.timedelta):
            return self._tz_now() + time
        if isinstance(time, datetime.time):
            date_time = datetime.datetime.combine(
                datetime.datetime.now(tz=time.tzinfo or self.sch.timezone).date(), time
            )
            if date_time.tzinfo is None:
                date_time = self.sch.timezone.localize(date_time)
            if shift_day and date_time <= datetime.datetime.now(pytz.utc):
                date_time += datetime.timedelta(days=1)
            return date_time
        # isinstance(time, datetime.datetime):
        return time

    def run_repeating(
            self,
            callback: Callable[[str], None],
            interval: Union[float, datetime.timedelta],
            first: Union[float, datetime.timedelta, datetime.datetime, datetime.time] = None,
            last: Union[float, datetime.timedelta, datetime.datetime, datetime.time] = None,
            context: dict = None,
            name: str = None,
            job_kwargs: dict = None,
    ) -> Job:

        if not job_kwargs:
            job_kwargs = {}

        name = name or callback.__name__
        job = Job(callback, context, name, self)

        dt_first = self.parse_time_input(time=first)
        dt_last = self.parse_time_input(time=last)

        if dt_last and dt_first and dt_last < dt_first:
            raise ValueError("'last' must not be before 'first'!")

        if isinstance(interval, datetime.timedelta):
            interval = interval.total_seconds()

        j = self.sch.add_job(
            callback,
            trigger='interval',
            kwargs=context,
            start_date=dt_first,
            end_date=dt_last,
            seconds=interval,
            name=name,
            **job_kwargs,
        )

        job.job = j
        return job


# class Bot():
#     def Hello(self):
#         print("hello")
#
# def helloworld(bot: Bot):
#     bot.Hello()
#
#
# def main():
#     bot = Bot()
#     r = JobQueue()
#
#     r.run_repeating(
#         helloworld,
#         interval=datetime.timedelta(seconds=3),
#         context={"bot": bot}
#     )
#
#     print("running")
#
#     r.start()
#     while True:
#         time.sleep(0.5)
#
#     print("end")
#
#     r.stop()
#
#
#
#
# if __name__ == "__main__":
#     main()