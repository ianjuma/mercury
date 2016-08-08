#! /usr/bin/python

import gevent
from apscheduler.schedulers.gevent import GeventScheduler

from services.bulkSMSService import BulkSMSService

import logging
import redis
import datetime
import settings

r = redis.StrictRedis(host='localhost', port=6379, db=0)

import newrelic.agent
application = newrelic.agent.application()


class App:
    @newrelic.agent.background_task(application)
    def run(self):
        date      = r.get('CrunchDate')
        date_1    = datetime.datetime.strptime(date, "%Y-%m-%d")

        next_date = str((date_1 + datetime.timedelta(days = 1))).split(' ')[0]

        r.set('CrunchDate', next_date)

        service = BulkSMSService()
        # services = [services]
        # map(s.fetch, services)
        # x foreach - x.fetch
        service.fetchStats(
            username = None,
            date = date
        )


if __name__ == '__main__':
    logging.basicConfig()

    app = App()
 
    scheduler = GeventScheduler()
    scheduler.add_job(app.run, 'interval', minutes=3, id='stats')

    g = scheduler.start()

    try:
        g.join()
    except (KeyboardInterrupt, SystemExit):
        pass
