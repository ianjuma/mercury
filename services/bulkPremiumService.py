#! /usr/bin/python

from baseService import BaseService


class BulkSMSService(BaseService):

    def processResponse(self, response):
        print response

    def processUserResponse(self, response):
        print response
