from apscheduler.schedulers.background import BackgroundScheduler


class Manager(object):

    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()

    def schedule(self, function=None, **kwargs):
        self.sched.add_job(function, 'cron', **kwargs)
