#! /usr/bin/python

import gevent

import gevent.monkey
gevent.monkey.patch_socket()

from actor import Actor

import os

import requests
import gevent


class BaseService(Actor):
    base_url = 'http://134.213.60.56:8080/'
    view     = ''

    def build_url(self, username = None):
        if username is None:
            return self.base_url + self.view
        else:
            # urlencode
            return self.base_url + self.view + "&" +username

    def fetch_url(self, url):
        headers = { 'apikey': os.getenv('APIKEY') }

        r = requests.get(url, headers = headers)
        resp = r.json()
        return resp

    def grequest_user(self, username):
        print self.build_url(username)
        thread = gevent.spawn( self.fetch_url,  self.build_url(username = username) )
        thread.join()

        self.processUserResponse( thread.value )

    def grequest(self):
        print self.build_url(None)
        thread = gevent.spawn( self.fetch_url,  self.build_url(username = None) )
        thread.join()

        self.processResponse( thread.value )

    def processResponse(self, response):
        raise NotImplemented

    def processUserResponse(self, response):
        raise NotImplemented

    def receive(self, message):
        self.grequest()
        gevent.sleep(0)
