#! /usr/bin/python

import gevent
from services.bulkSMSService import BulkSMSService

from os.path import join, dirname
from dotenv import load_dotenv

import polling


class App:
    def run(self):
       service = BulkSMSService()
       service.grequest()


if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    app = App()

    polling.poll(
        lambda: app.run(),
        step=60,
        poll_forever=True
    )
