#!/usr/bin/env python

import SocketServer
import urlparse
import urllib
import requests
import os

from collections import namedtuple

SparkFunDataEndpoint = namedtuple(
    'SparkFunDataEndpoint', 'public_key,private_key')

FILTER_IP = os.environ['FILTER_IP']
SPARKFUN_PUBLIC_KEY = os.environ['SPARKFUN_PUBLIC_KEY']
SPARKFUN_PRIVATE_KEY = os.environ['SPARKFUN_PRIVATE_KEY']

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 12334


class MyTCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        self.data = self.rfile.readline().strip()

        if FILTER_IP != self.client_address[0]:
            print('Dropping {} bytes from `{}`'.format(
                len(self.data), self.client_address[0]))
            return

        self._write(self.data)
        self.wfile.write('OK')

    def _write(self, data):
        """
        data expected to be like:
        'temperature_1=123&temperature_2=456'
        """
        query_params = {'private_key': SPARKFUN_PRIVATE_KEY}
        query_params.update(urlparse.parse_qsl(data))

        url = 'http://data.sparkfun.com/input/{public_key}?{params}'.format(
            public_key=SPARKFUN_PUBLIC_KEY,
            params=urllib.urlencode(query_params))

        print("POST {}".format(url))
        response = requests.post(url)
        response.raise_for_status()

if __name__ == "__main__":

    server = SocketServer.TCPServer((LISTEN_HOST, LISTEN_PORT), MyTCPHandler)
    server.serve_forever()
