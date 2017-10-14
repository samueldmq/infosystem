from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler(BackgroundScheduler):

    def __init__(self):
        super().__init__()
        self.start()

    def schedule(self, callback, **kwargs):
        self.add_job(callback, 'cron', **kwargs)

    def hourly(self, callback, minute=0):
        self.add_job(callback, 'cron', minute=minute)

    def daily(self, callback, hour=0, minute=0):
        self.add_job(callback, 'cron', hour=hour, minute=minute)

    def weekly(self, callback, day='mon', hour=0, minute=0):
        if day not in ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'):
            raise ValueError
        self.add_job(
            callback, 'cron', day_of_week=day, hour=hour, minute=minute)

    def monthly(self, callback, day=1, hour=0, minute=0):
        self.add_job(callback, 'cron', day=day, hour=hour, minute=minute)
