#!/usr/bin/env python3
from Adafruit_MAX31856 import max31856
import HPADDA
import matplotlib.pyplot as plt
'''Multi channel (7 ch for Voltage, 4 ch for temperature)'''

from time import sleep
import datetime
from logging import getLogger, StreamHandler, DEBUG, Formatter, INFO
import argparse
from multiprocessing import Process
#
import matplotlib
matplotlib.use('Agg')

# logger
logger = getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
formatter = Formatter(fmt)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False


def pressure(volt):
    '''Return the pressure (mbar) from the monitor voltage'''
    exponent = int(volt) - 11
    mantissa = ((volt - int(volt)) + .1) / .11
    return mantissa * 10**exponent


def read_temperatures():
    '''Return temperatue data.

    '''
    external = [thermos[i].read_temp_c() for i in range(4)]
    internal = [thermos[i].read_internal_temp_c() for i in range(4)]
    ret = []
    for i in range(4):
        ret.append((external[i], internal[i]))
    return ret


def read_ion_gauge(chamber=0):
    '''Read ion gauge data

    Parameters
    -----------
    chamber: int
        0: Analysis
        1: Preparation

    Return
    -------
    float
        Pressure (mbar)
    '''
    voltage = adda.get_voltage(chamber + 1)
    return pressure(voltage)


save_fmt = '{}\t{:6.3f}\t{:6.3f}\t{:6.3f}\t{:6.3f}'
save_fmt += '\t{:.3e}\t{:.3e}\t{:6.3f}\t{:6.3f}\t{:6.3f}'


def read_and_save():
    '''Read the values and save them
    '''
    temperatures = read_temperatures()
    ana_pres = read_ion_gauge(0)
    prep_pres = read_ion_gauge(1)
    v3 = adda.get_voltage(5)
    v4 = adda.get_voltage(6)
    v5 = adda.get_voltage(7)
    temp_fmt = 'Temperature at {}: {:6.3f} C (internal {:6.3f} C)'
    pressure_fmt = '{:.3e} mbar'
    voltage_fmt = '{:5.2f} V'
    for i in range(4):
        logger.info(temp_fmt.format(i,
                                     temperatures[i][0],
                                     temperatures[i][1]))
    logger.info('Analysis: ' + pressure_fmt.format(ana_pres))
    logger.info('Preparation: ' + pressure_fmt.format(prep_pres))
    logger.info('Voltage-3:' + voltage_fmt.format(v3))
    logger.info('Voltage-4:' + voltage_fmt.format(v4))
    logger.info('Voltage-5:' + voltage_fmt.format(v5))
    now = datetime.datetime.now()
    logfile.write(save_fmt.format(now.strftime('%Y-%m-%d %H:%M:%S'),
                                  temperatures[0][0], temperatures[1][0],
                                  temperatures[2][0], temperatures[3][0],
                                  ana_pres, prep_pres, v3, v4, v5))
    with open('lastread.dat', mode='w') as lastread:
        lastread.write(save_fmt.format(now.strftime('%Y-%m-%d %H:%M:%S'),
                                       temperatures[0][0], temperatures[1][0],
                                       temperatures[2][0], temperatures[3][0],
                                       ana_pres, prep_pres, v3, v4, v5))

    return (now, temperatures[0][0], temperatures[1][0],
            temperatures[2][0], temperatures[3][0],
            ana_pres, prep_pres, v3, v4, v5)


def draw_graphs(data):
    """1st column が datetime オブジェクトの2Dデータを読み込んでグラフにする。"""
    logger.debug('len(data[0]) is {}'.format(data[0]))
    logger.debug('len(data[1]) is {}'.format(data[1]))
    logger.debug('len(data[2]) is {}'.format(data[2]))
    logger.debug('len(data[3]) is {}'.format(data[3]))
    logger.debug('len(data[4]) is {}'.format(data[4]))
    logger.debug('len(data[5]) is {}'.format(data[5]))
    logger.debug('len(data[6]) is {}'.format(data[6]))
    logger.debug('len(data[7]) is {}'.format(data[7]))
    logger.debug('len(data[8]) is {}'.format(data[8]))
    logger.debug('len(data[9]) is {}'.format(data[9]))
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
    ax2.plot_date(data[0], data[5], color='red',
                  fmt='-', label='Analysis Pressure')
    ax2.plot_date(data[0], data[6], color='blue',
                  fmt='-', label='Preparation Pressure')
    ax2.set_ylabel('Pressure  (mbar)')
    ax2.legend(loc=2)
    ax2.set_yscale('log')
    #
    ax3 = fig.add_subplot(223)
    ax3.plot_date(data[0], data[7],
                  fmt='-', label='V3')
    ax3.plot_date(data[0], data[8],
                  fmt='-', label='V4')
    ax3.plot_date(data[0], data[9],
                  fmt='-', label='V5')
    ax3.set_ylabel('Voltage  (V)')
    ax3.legend(loc=2)
    #
    #
    plt.subplots_adjust(top=0.98, right=0.98, left=0.05, bottom=0.05,
                        wspace=.1)
    plt.savefig('Logdata.png')
    plt.close()
    return True


adda = HPADDA.Board()
adda.set_sample_rate(300)
thermos = [max31856.MAX31856(software_spi={'clk': 25, 'cs': 14,
                                           'do': 8, 'di': 7}),
           max31856.MAX31856(software_spi={'clk': 25, 'cs': 15,
                                           'do': 8, 'di': 7}),
           max31856.MAX31856(software_spi={'clk': 25, 'cs': 16,
                                           'do': 8, 'di': 7}),
           max31856.MAX31856(software_spi={'clk': 25, 'cs': 21,
                                           'do': 8, 'di': 7})]

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    epilog="""
NOTE: あとでちゃんと書く。""")
parser.add_argument('--logfile',
                    type=str, default=None,
                    help='''Log filename''')
args = parser.parse_args()
if args.logfile:
    logfile = open(args.logfile, mode='w')
    logfile.write('#date\tT1\tT2\tT3\tT4\t\Pressure(A)\tPressure(P)\t')
    logfile.write('v3\tv4\v5\n')
else:
    logfile = open('log.txt', mode='w+')

data = [[],
        [], [], [], [],
        [], [],
        [], [], []]
maxdatalength = 300
drawevery = 5  # seconds
sleepingtime = 1  # seconds
try:
    while True:
        a_read = read_and_save()
        [data[i].append(a_read[i]) for i in range(len(a_read))]
        if len(data[0]) > maxdatalength:
            for i in range(len(a_read)):
                del data[i][0]
        now = datetime.datetime.now()
        if now.second % drawevery == 0:
            p = Process(target=draw_graphs, args=(data,))
            p.start()
        sleep(sleepingtime)
except KeyboardInterrupt:
    logfile.close()
