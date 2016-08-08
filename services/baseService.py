#! /usr/bin/python

import gevent

import gevent.monkey
gevent.monkey.patch_socket()

import settings

import requests
import gevent
from urllib import urlencode


class BaseService:
    base_url = settings.base_url
    date     = ''

    def build_url(self, username = None):
        if username is None:
            return self.base_url + self.get_view()
        else:
            f = { 'username': username }
            return self.base_url + self.get_view() + "&" + urlencode(f)

    def fetch_(self, url):
        headers = { 'apikey': settings.api_key }

        r = requests.get(url, headers = headers)
        resp = r.json()
        return resp

    def fetchStats(self, username, date):
        # change date so view can update
        self.date = date

        if username is not None:
            thread = gevent.spawn( self.fetch_,  self.build_url(username = username) )
            thread.join()
            return self.processUserResponse( thread.value, username )
        else:
            thread = gevent.spawn( self.fetch_,  self.build_url(username = None) )
            thread.join()
            return self.processResponse( thread.value )

    def get_view(self):
        raise NotImplemented

    def processResponse(self, response):
        raise NotImplemented

    def processUserResponse(self, response):
        raise NotImplemented
