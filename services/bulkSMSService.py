#! /usr/bin/python

from baseService import BaseService
from queue import enqueue

from gevent import greenlet


class BulkSMSService(BaseService):
    def get_view(self):
        return 'bulkSms/sent?granularity=day&metric=cost&currencyCode=USD&' + \
                  'startDate={}&endDate={}'.format(self.date, self.date)

    def processResponse(self, response):
      for username in response.get('responses').get('userStats')[0].get('elements'):
          self.fetchStats(
              username = username, 
              date = self.date
          )

    def processUserResponse(self, response, username):
        for stat in response.get('responses').get('networkStats'):
          date = stat.get('date')

          for destination, amount in stat.get('elements').items():
              country = destination.split(' ')[0]
              network = destination.split(' ')[1].strip("()")
              cost    = amount.split(' ')[1]
              # add to bd - amount, username, date
              res = enqueue.add_stat.delay(username, date, network, country, cost)
