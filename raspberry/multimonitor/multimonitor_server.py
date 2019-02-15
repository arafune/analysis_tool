#!/usr/bin/env python3
"""Multimonitor server"""

import argparse
from logging import DEBUG, INFO, WARN, Formatter, StreamHandler, getLogger
from multiprocessing import Process
from time import sleep

import ambient
from flask import Flask, render_template, request
from gevent import pywsgi

import output as output
# import multimonitor.sensor as sensor
from geventwebsocket.handler import WebSocketHandler

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
