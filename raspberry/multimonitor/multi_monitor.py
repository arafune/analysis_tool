#!/usr/bin/env python3
"""Multi monitor module."""

import argparse
from logging import DEBUG, INFO, WARN, Formatter, StreamHandler, getLogger
from multiprocessing import Process
from time import sleep

import ambient

import output as output
import sensor_set_a as sensors

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


def send2ambient(data):
    """Send pressure data to Ambient."""
    channelID = '8775'
    readkey = '6396addf4ce692fa'
    writekey = '18c9d6f2a7824fa1'
    userkey = '5541fb66d3f9f20dd6'
    am = ambient.Ambient(channelID, writekey, readkey, userkey)
    am.send({'created': data[0], 'd1': data[1], 'd2': data[2]})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
    NOTE: あとでちゃんと書く。""")
    parser.add_argument(
        '--logfile', type=str, default=None, help='''Log filename''')
    args = parser.parse_args()
    if args.logfile:
        logfile = open(args.logfile, mode='w')
        logfile.write('#date\tT1\tT2\tT3\tT4\tPressure(A)\tPressure(P)\t')
        logfile.write('v3\tv4\v5\n')
    else:
        logfile = open('output_log.txt', mode='w+')
        logfile.write('#date\tT1\tT2\tT3\tT4\tPressure(A)\tPressure(P)\t')
        logfile.write('v3\tv4\v5\n')
    #
    data = [[] for i in range(10)]
    maxdatalength = 300
    drawevery = 5  # seconds
    sleepingtime = 1  # seconds
    try:
        while True:
            a_read = sensors.read(9)
            [data[i].append(a_read[i]) for i in range(len(a_read))]
            if len(data[0]) > maxdatalength:
                for i in range(len(a_read)):
                    del data[i][0]
            output.publish(a_read, logfile)
            if a_read[0].second % drawevery == 0:
                p = Process(target=output.graphs, args=(data, ))
                p.start()
            if a_read[0].second == 0:
                logger.debug('type a_read[0] {}'.format(type(a_read[0])))
                logger.debug('a_read[0] {}'.format(a_read[0]))
                senddata = (a_read[0].strftime('%Y-%m-%d %H:%M:%S'), a_read[5],
                            a_read[6])
                p2 = Process(target=send2ambient, args=(senddata, ))
                logger.debug('send_data: {}, {}, {}'.format(
                    senddata[0], senddata[1], senddata[2]))
                p2.start()
            sleep(sleepingtime)
    except KeyboardInterrupt:
        logfile.close()
