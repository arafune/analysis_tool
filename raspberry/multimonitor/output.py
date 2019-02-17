#!/usr/env/bin python3
"""Module for multimonitor (non-device depndent)."""

import argparse
import datetime
from json import dumps
from logging import DEBUG, INFO, WARN, Formatter, StreamHandler, getLogger
from multiprocessing import Process
from random import random
from time import mktime, sleep

import matplotlib
import matplotlib.pyplot as plt
import ambient

matplotlib.use('Agg')

LOGLEVEL = WARN
logger = getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
formatter = Formatter(fmt)
handler = StreamHandler()
handler.setLevel(LOGLEVEL)
logger.setLevel(LOGLEVEL)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False


def dummy(n_ch):
    """Return random data.

    n_ch: int
        number of channels

    """
    data = [datetime.datetime.now()]
    data[1:] = [random() for a in range(n_ch)]
    return data


def publish(a_read, logfile):
    """Publish the data strings."""
    save_fmt = '{}\t{:6.3f}\t{:6.3f}\t{:6.3f}\t{:6.3f}'
    save_fmt += '\t{:.3e}\t{:.3e}\t{:6.3f}\t{:6.3f}\t{:6.3f}\n'
    html_fmt = '{} <br>\n'
    logfile.write(
        save_fmt.format(a_read[0].strftime('%Y-%m-%d %H:%M:%S'), a_read[1],
                        a_read[2], a_read[3], a_read[4], a_read[5], a_read[6],
                        a_read[7], a_read[8], a_read[9]))


def json(a_read):
    """Return json format data."""
    #    print(int(mktime(a_read[0].timetuple())))
    t = int(mktime(a_read[0].timetuple()))
    json_dump = dumps([{
        'time': t,
        'y': a_read[1]
    }, {
        'time': t,
        'y': a_read[2]
    }])

    #    json_dump = dumps({
    #        'readdata': {
    #            'date': int(mktime(a_read[0].timetuple())),
    #            'T1': a_read[1],
    #            'T2': a_read[2],
    #            'T3': a_read[3],
    #            'T4': a_read[4],
    #            'Pres_A': a_read[5],
    #            'Pres_P': a_read[6],
    #            'V3': a_read[7],
    #            'V4': a_read[8],
    #            'V5': a_read[9]
    #    })

    logger.info('json format: {}'.format(json_dump))
    return json_dump


def send2ambient(data):
    """Send pressure data to Ambient."""
    channelID = '8775'
    readkey = '6396addf4ce692fa'
    writekey = '18c9d6f2a7824fa1'
    userkey = '5541fb66d3f9f20dd6'
    am = ambient.Ambient(channelID, writekey, readkey, userkey)
    am.send({'created': data[0], 'd1': data[1], 'd2': data[2]})


def graphs(data):
    """Draw graph.

    Parameters
    ----------
    data: list
        2D-list. The first column should be datetime object.

    """
    #    for i in range(10):
    #        logger.debug('len(data[{}]) is {}'.format(i, data[i]))
    fig = plt.figure(figsize=(15, 10))
    #
    ax1 = fig.add_subplot(221)
    ax1.plot_date(data[0], data[1], fmt='-', label='T_Phoibos')
    ax1.plot_date(data[0], data[2], fmt='-', label='T_Analyis')
    ax1.plot_date(data[0], data[3], fmt='-', label='T_Prep.')
    ax1.plot_date(data[0], data[4], fmt='-', label='T_AUX')
    ax1.legend(loc=2)
    ax1.set_ylabel('Temperature  (C)')
    #
    ax2 = fig.add_subplot(222)
    ax2.plot_date(
        data[0], data[5], color='red', fmt='-', label='Analysis Pressure')
    ax2.plot_date(
        data[0], data[6], color='blue', fmt='-', label='Preparation Pressure')
    ax2.set_ylabel('Pressure  (mbar)')
    ax2.legend(loc=2)
    ax2.set_yscale('log')
    #
    ax3 = fig.add_subplot(223)
    ax3.plot_date(data[0], data[7], fmt='-', label='V3')
    ax3.plot_date(data[0], data[8], fmt='-', label='V4')
    ax3.plot_date(data[0], data[9], fmt='-', label='V5')
    ax3.set_ylabel('Voltage  (V)')
    ax3.legend(loc=2)
    #
    plt.subplots_adjust(
        top=0.98, right=0.98, left=0.05, bottom=0.05, wspace=.1)
    plt.savefig('Logdata.png')
    plt.close()
    return True


if __name__ == '__main__':
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
            a_read = dummy(9)
            [data[i].append(a_read[i]) for i in range(len(a_read))]
            if len(data[0]) > maxdatalength:
                for i in range(len(a_read)):
                    del data[i][0]
            publish(a_read, logfile)
            if a_read[0].second % drawevery == 0:
                p = Process(target=graphs, args=(data, ))
                p.start()
#            if a_read[0].second == 0:
#                logger.debug('type a_read[0] {}'.format(type(a_read[0])))
#                logger.debug('a_read[0] {}'.format(a_read[0]))
#                senddata = (a_read[0].strftime('%Y-%m-%d %H:%M:%S'),
#                             a_read[5], a_read[6])
#                p2 = Process(target=send2ambient, args=(senddata, ))
#                logger.debug('send_data: {}, {}, {}'.format(
#                    senddata[0], senddata[1], senddata[2]))
#                p2.start()
            sleep(sleepingtime)
    except KeyboardInterrupt:
        logfile.close()
