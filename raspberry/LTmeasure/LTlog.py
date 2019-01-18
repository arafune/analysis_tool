#!/usr/bin/env python3
# coding:
"""LakeShore 330 から温度データを読み込んで、png ファイルフォーマットのグラフを出力する。"""

import datetime
import argparse
import matplotlib.pyplot as plt
import random


def build_dummydate():
    data = []
    with open('dummydata.dat') as f:
        for line in f:
            l = line.split('\t')
            datetime.datetime.strptime(l[0],
                                       '%Y-%m-%d %H:%M:%S')
            singledata = [datetime.datetime.strptime(l[0],
                                                     '%Y-%m-%d %H:%M:%S'),
                          float(l[1]),
                          float(l[2])]
            data.append(singledata)
            data = list(zip(*data))
    return data


def read_dummy(n_ch):
    '''Return random data

    n_ch: number of channels
    '''
    data = [datetime.datetime.now()]
    data[1:1] = [random.random() for a in range(n_ch)]
    return data


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
