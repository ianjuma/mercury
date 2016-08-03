from celery import Celery
from celery import Task

app = Celery('stats')


class Persist(Task):
    def run(self, **kargs):
        pass


@app.task
def addTask(**obj):
    # add to db
    pass


if __name__ == '__main__':
    app.worker_main()
