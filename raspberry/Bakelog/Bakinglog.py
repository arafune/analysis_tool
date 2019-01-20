#!/usr/bin/env python3
# coding:
"""
Bakinglog

チャンバーの温度と真空度（に対応する電圧）を読んでpngファイルフォーマットのグラフを出力する。"""

import datetime
import argparse
import matplotlib.pyplot as plt
import random
import sys
from time import sleep

dummy = True


def read_dummy(n_ch):
    '''Return random data

    n_ch: number of channels
    '''
    data = [datetime.datetime.now()]
    data[1: 1] = [random.random() for a in range(n_ch)]
    return data


def get_data(dummy=False):
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
        return read_dummy(4)
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


def draw_pressure_temperature(data):
    """1st column が datetime オブジェクトの2Dデータを読み込んでグラフにする。"""
    fig = plt.figure(figsize=(30, 10))
    plt.subplots_adjust(top=0.98, right=0.98, left=0.05, bottom=0.05)
    #
    ax1 = fig.add_subplot(111)
    ax1.plot_date(data[0], data[1], fmt='-', label='Analysis Pressure')
    ax1.plot_date(data[0], data[2], fmt='-', label='Preparation Pressure')
    ax1.set_yscale('log')
    ax1.legend(loc=2)
    #
    ax2 = fig.add_subplot(122)
    ax2.plot_date(data[0], data[3], fmt='-', label='temperature_phoibos')
    ax2.plot_date(data[0], data[4], fmt='-', label='temperature_Analyis')
    ax2.legend(loc=2)
    plt.savefig('BakingLogdata.png')
    plt.close()
    return True


if __name__ == '__main__':
    logfile = 'BakingLog.dat'
    lastread = 'lastread.dat'
    maxdatalength = 300
    drawevery = 5  # seconds
    sleepingtime = 1  # seconds
    #
    data = [[], [], [], [], []]
    try:
        while True:
            now, p_Analysis, p_Prep, tempA, tempB = get_data(dummy=dummy)
            data[0].append(now)
            data[1].append(p_Analysis)
            data[2].append(p_Prep)
            data[3].append(tempA)
            data[4].append(tempB)
            if len(data[0]) > 300:
                del data[0][0]
                del data[1][0]
                del data[2][0]
                del data[3][0]
                del data[4][0]
            nowstr = now.strftime('%Y-%m-%d %H:%M:%S')
            print(nowstr, p_Analysis, p_Prep, tempA, tempB)
            with open(lastread, mode='w') as f:
                str = '{}\n{:.2f}\n{:.2f}\n{:.2f}\n{:.2f}\n'.format(
                    nowstr, p_Analysis, p_Prep, tempA, tempB)
                f.write(str)
            with open(logfile, mode='a') as f:
                str = '{}\n{:.2f}\n{:.2f}\t{:.2f}\t{:.2f}\n'.format(
                    nowstr, p_Analysis, p_Prep, tempA, tempB)
                f.write(str)
            if now.second % drawevery == 0:
                draw_pressure_temperature(data)
            else:
                sleep(sleepingtime)
    except KeyboardInterrupt:
        if not dummy:
            pass
        sys.exit()
