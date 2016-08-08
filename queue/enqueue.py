from celery import Celery
from celery import Task
from celery.decorators import task

import MySQLdb
conn = MySQLdb.connect(
    host= "localhost",
    user="root",
    passwd="root",
    db="tableau"
)

con = conn.cursor()

app = Celery('queue', broker='redis://localhost', result='redis://localhost:6379/0')

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Africa/Nairobi',
    CELERY_ENABLE_UTC=True,
    CELERY_ANNOTATIONS = {
      'enqueue.add_stat': {'rate_limit': '1000/m'}
    }
)


@app.task
def add_stat(username, date, network, country, cost):
    def run(self, **kargs):
        try:
             con.execute("""INSERT INTO bulk_sms_networks_cost VALUES(%s, %s, 
                 %s, %s, %d)""", (username, date, network, country, cost) )
             res = con.commit()
             return res
        except:
             res = con.rollback()
             return res
