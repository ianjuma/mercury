#! /usr/bin/python

from baseService import BaseService


class BulkSMSService(BaseService):
    view = 'bulkSms/sent?granularity=day&metric=cost&currencyCode=USD&' + \
                  'startDate=2015-07-11&endDate=2015-07-11'

    def processResponse(self, response):
      for username in response.get('responses').get('userStats')[0].get('elements'):
          self.grequest_user(username)

    def processUserResponse(self, response):
        print response
