#!/usr/bin/env python3
"""Multimonitor server."""

from logging import DEBUG, INFO, WARN, Formatter, StreamHandler, getLogger
from time import sleep

# import ambient
from flask import Flask, render_template, request
from gevent import pywsgi
# import multimonitor.sensor as sensor
from geventwebsocket.handler import WebSocketHandler

import output as output

# logger
LOGLEVEL = INFO
logger = getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
formatter = Formatter(fmt)
handler = StreamHandler()
handler.setLevel(LOGLEVEL)
logger.setLevel(LOGLEVEL)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False

app = Flask(__name__)


@app.route('/')
def index():
    """Set index.

    make 'templates' directory and then put 'index.html' file in it.
    (Its Flask's rule!)
    """
    return render_template('index.html')


@app.route('/publish')
def publish():
    """Output websocket."""
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            read = output.json(output.dummy(9))
            #            print('read: {}'.format(read))
            ws.send(read)
            sleep(1)
    return


if __name__ == '__main__':
    app.debug = True
    server = pywsgi.WSGIServer(('localhost', 8000),
                               app,
                               handler_class=WebSocketHandler)
    server.serve_forever()
