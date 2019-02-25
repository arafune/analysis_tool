#!/usr/bin/env python3
"""Measure/Store data module for the multimonitor."""

import os
from multiprocessing import Process
from time import sleep

import output

dummy = False
try:
    import sensor_set_a
except ImportError:
    dummy = True

interval_time = 3  # second


def header(logfile_name):
    """Write header of log file.

    Parameters
    ----------
    logfile_name: str
        File for log.

    """
    if os.path.isfile(logfile_name):
        return
    with open(logfile_name, mode='a+') as logfile:
        logfile.write('#date\tT1\tT2\tT3\tT4\tPressure(A)\tPressure(P)\t')
        logfile.write('v3\tv4\tv5\n')


def single(logfile_name):
    """Read values from sensors, and send data to Ambient.

    Read the Temperatures from 4ch sensor, Pressure from Varian
    ion gauge, and AUX Voltages from 3ch.

    Parameters
    ----------
    logfile_name: str
        Filename for log

    """
    if dummy:
        now, t1, t2, t3, t4, ana, prep, v3, v4, v5 = output.dummy(9)
    else:
        now, t1, t2, t3, t4, ana, prep, v3, v4, v5 = sensor_set_a.read()
        if now.second < interval_time:
            senddata = (now.strftime('%Y-%m-%d %H:%M:%S'), ana * 1E10,
                        prep * 1E10, t1, t2, t3, t4)
            proc = Process(target=output.send2ambient, args=(senddata, ))
            proc.start()
    output.publish((now, t1, t2, t3, t4, ana, prep, v3, v4, v5),
                   logfile=logfile_name)


def continuous(logfile_name, sleeping_time=1):
    """Read sensors continuously, and store them."""
    while True:
        single(logfile_name)
        sleep(sleeping_time)


if __name__ == '__main__':
    logfile_name = 'log.txt'
    header(logfile_name)
    continuous(logfile_name, sleeping_time=interval_time)
