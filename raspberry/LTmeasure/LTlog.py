#!/usr/bin/env python3
# coding:
"""LakeShore 330 から温度データを読み込んで、png ファイルフォーマットのグラフを出力する。"""

import datetime
import argparse
import matplotlib.pyplot as plt
import random
import sys
from time import sleep
try:
    import Gpib
except ModuleNotFoundError:
    dummy = True


def build_dummydate():
    data = []
    with open('dummydata.dat') as f:
        for line in f:
            now, temp1, temp2 = line.split('\t')
            data.append(
                [datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S'),
                 float(temp2), float(temp2)])
            data = list(zip(*data))
    return data


def read_dummy(n_ch):
    '''Return random data

    n_ch: number of channels
    '''
    data = [datetime.datetime.now()]
    data[1: 1] = [random.random() for a in range(n_ch)]
    return data


def init_lakeshore330(address=12):
    try:
        inst = Gpib.Gpib(0, address, timeout=60)
    except NameError:  # <<< FIXME
        return False
    inst.write("*IDN?")
    if 'LSCI,MODEL330' in inst.read(100):
        inst.write('CCHN A')
        inst.write('CUNI K')
        inst.write('SUNI K')
        inst.write('*OPC')
        inst.write('CCHN B')
        inst.write('CUNI K')
        inst.write('SUNI K')
        inst.write('*OPC')
        return True
    else:
        return False


def terminate_lakeshore330(address=12):
    inst = Gpib.Gpib(0, address, timeout=60)
    inst.write('*RST')
    inst.write('*CLS')
    return True


def get_temperature(address=12, dummy=False):
    '''Get temperatures from Lakeshore 330

    address: int
        Gpib address (default 12)

    dummy: boolean
        Return random values, not using gpib. For test.

    Returns
    ---------
         (datetime object, temperature, temperature)
    '''
    if dummy:
        return read_dummy(2)
    else:
        inst = Gpib.Gpib(0, address, timeout=60)
        now = datetime.datetime.now()
        inst.write('SCHN A')
        inst.write('SDAT?')
        temperature_a = inst.read(1024)
        inst.write('SCHN B')
        inst.write('SDAT?')
        temperature_b = inst.read(1024)
        return(now, float(temperature_a), float(temperature_b))


def draw_lakeshore330(data):
    """1st column が datetime オブジェクトの2Dデータを読み込んでグラフにする。"""
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)
    plt.subplots_adjust(top=0.98, right=0.98, left=0.05, bottom=0.05)
    ax.plot_date(data[0], data[1], fmt='-', label='Upper sensor')
    ax.plot_date(data[0], data[2], fmt='-', label='Lower sensor')
    ax.legend(loc=2)
    plt.savefig('LTdata.png')
    plt.close()
    return True


if __name__ == '__main__':
    logfile = 'LTlog.dat'
    lastread = 'lastread.dat'
    maxdatalength = 300
    drawevery = 5  # seconds
    sleepingtime = 1  # seconds
    #
    if not init_lakeshore330(12):
        dummy = True
    data = [[], [], []]
    try:
        while True:
            now, tempA, tempB = get_temperature(dummy=dummy)
            data[0].append(now)
            data[1].append(tempA)
            data[2].append(tempB)
            if len(data[0]) > 300:
                del data[0][0]
                del data[1][0]
                del data[2][0]
            nowstr = now.strftime('%Y-%m-%d %H:%M:%S')
            print(nowstr, tempA, tempB)
            with open(lastread, mode='w') as f:
                str = '{}\n{:.2f}\n{:.2f}\n'.format(nowstr, tempA, tempB)
                f.write(str)
            with open(logfile, mode='a') as f:
                str = '{}\t{:.2f}\t{:.2f}\n'.format(nowstr, tempA, tempB)
                f.write(str)
            if now.second % drawevery == 0:
                draw_lakeshore330(data)
            else:
                sleep(sleepingtime)
    except KeyboardInterrupt:
        if not dummy:
            terminate_lakeshore330()
        sys.exit()
