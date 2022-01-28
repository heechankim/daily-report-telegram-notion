from pytz import timezone
import time
from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:

    def start(self):
        self.sch = BackgroundScheduler()
        self.sch.configure(timezone=timezone('Asia/Seoul'))
        self.sch.start()
        self.sch.add_job(
            self.job1,
            'interval',
            seconds=10,
            max_instances=1
        )

    def job1(self):
        with open('./test.txt', mode='a') as f:
            f.write(time.strftime('%c', time.localtime(time.time())) + "\n")
