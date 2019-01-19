#!/usr/bin/env python3
# coding:
"""LakeShore 330 から温度データを読み込んで、png ファイルフォーマットのグラフを出力する。"""

import datetime
import argparse
import matplotlib.pyplot as plt
import random
import Gpib


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
    inst = Gpib.Gpib(0, address, timeout=60)
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
    inst = Gpib.Gpib(0, address, timeout=60)
    if dummy:
        return read_dummy(2)
    else:
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
    fig = plt.figure(figsize=(15, 10), dpi=200)
    ax = fig.add_subplot(111)
    ax.plot_date(data[0], data[1], fmt='-', label='Upper sensor')
    ax.plot_date(data[0], data[2], fmt='-', label='Lower sensor')
    ax.legend(loc=2)
    plt.savefig('LTdata.png')


if __name__ == '__main__':
    pass
