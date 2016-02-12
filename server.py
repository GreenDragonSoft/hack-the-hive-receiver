#!/usr/bin/env python

import SocketServer
import urlparse
import urllib
import os

from collections import namedtuple

SparkFunDataEndpoint = namedtuple(
    'SparkFunDataEndpoint', 'public_key,private_key')

SECRET_DEVICE_ID = os.environ['SECRET_DEVICE_ID']
SPARKFUN_PUBLIC_KEY = os.environ['SPARKFUN_PUBLIC_KEY']
SPARKFUN_PRIVATE_KEY = os.environ['SPARKFUN_PRIVATE_KEY']

LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 11234


class MyTCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        self.data = self.rfile.readline().strip()

        self._write(self.data)
        self.wfile.write('OK')

    def _write(self, data):
        """
        data expected to be like:
        'version=1&secret_device_id=???&temperature_1=123&temperature_2=456'
        """
        received_data = dict(urlparse.parse_qsl(data))

        print('received_data from {}: {}'.format(
            self.client_address[0], received_data))

        assert received_data.pop('version') == '1', (
                "Invalid or missing version number in data.")

        assert received_data.pop('secret_device_id') == SECRET_DEVICE_ID, (
                "Invalid or missing secret key in data")

        received_data.update(
            {'private_key': SPARKFUN_PRIVATE_KEY})  # for Sparkfun

        url = 'http://data.sparkfun.com/input/{public_key}?{params}'.format(
            public_key=SPARKFUN_PUBLIC_KEY,
            params=urllib.urlencode(received_data))

        print("{}".format(url))
        urllib.urlopen(url)

if __name__ == "__main__":

    server = SocketServer.TCPServer((LISTEN_HOST, LISTEN_PORT), MyTCPHandler)
    server.serve_forever()
