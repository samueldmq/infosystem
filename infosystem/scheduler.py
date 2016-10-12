from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler(BackgroundScheduler):

    def __init__(self):
        super().__init__()
        self.start()

    def schedule(self, callback, **kwargs):
        self.add_job(callback, 'cron', **kwargs)
