#!/usr/bin/env python3
from Adafruit_MAX31856 import max31856
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
'''Multi channel (7 ch for Voltage, 4 ch for temperature)'''
import PiPyADC.pipyadc
from PiPyADC.ADS1256_definitions import *
from PiPyADC.pipyadc import ADS1256
from time import sleep
import datetime
from logging import getLogger, StreamHandler, DEBUG, Formatter, INFO, WARN
import argparse
from multiprocessing import Process
#

# logger
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

# Input pin for the potentiometer on the Waveshare Precision ADC board:
EXT0 = POS_AIN0|NEG_AINCOM
# Light dependant resistor of the same board:
EXT1 = POS_AIN1|NEG_AINCOM
# The other external input screw terminals of the Waveshare board:
EXT2, EXT3, EXT4 = POS_AIN2|NEG_AINCOM, POS_AIN3|NEG_AINCOM, POS_AIN4|NEG_AINCOM
EXT5, EXT6, EXT7 = POS_AIN5|NEG_AINCOM, POS_AIN6|NEG_AINCOM, POS_AIN7|NEG_AINCOM

# You can connect any pin as well to the positive as to the negative ADC input.
# The following reads the voltage of the potentiometer with negative polarity.
# The ADC reading should be identical to that of the POTI channel, but negative.
POTI_INVERTED = POS_AINCOM|NEG_AIN0

# For fun, connect both ADC inputs to the same physical input pin.
# The ADC should always read a value close to zero for this.
SHORT_CIRCUIT = POS_AIN0|NEG_AIN0

# Specify here an arbitrary length list (tuple) of arbitrary input channel pair
# eight-bit code values to scan sequentially from index 0 to last.
# Eight channels fit on the screen nicely for this example..
CH_SEQUENCE = (EXT1, EXT2, EXT5, EXT6, EXT7)
################################################################################j


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

save_fmt = '{}\t{:6.3f}\t{:6.3f}\t{:6.3f}\t{:6.3f}'
save_fmt += '\t{:.3e}\t{:.3e}\t{:6.3f}\t{:6.3f}\t{:6.3f}'
html_fmt = '{} <br>\n'
html_fmt += '{:6.3f} C, {:6.3f} C, {:6.3f} C,{:6.3f} C <br>\n'
html_fmt += '{:.3E} mbar (A), {:.3E} mbar (Prep)<br>\n'
html_fmt += '{:6.3f} V, {:6.3f} V, {:6.3f}V\n'


def read_and_save():
    '''Read the values and save them
    '''
    raw_channels = adda.read_sequence(CH_SEQUENCE)
    # 1.004543 should be tuned.
    voltages = [(i * adda.v_per_digit)/1.004543 for i in raw_channels] 
    temperatures = read_temperatures()
    ana_pres = pressure(voltages[0])
    prep_pres = pressure(voltages[1])
    v3 = voltages[2]
    v4 = voltages[3]
    v5 = voltages[4]
    temp_fmt = 'Temperature at {}: {:6.3f} C (internal {:6.3f} C)'
    pressure_fmt = '{:.3e} mbar'
    voltage_fmt = '{:9.7f} V'
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
    with open('lastread.html', mode='w') as lastread:
        lastread.write(html_fmt.format(now.strftime('%Y-%m-%d %H:%M:%S'),
                                       temperatures[0][0], temperatures[1][0],
                                       temperatures[2][0], temperatures[3][0],
                                       ana_pres, prep_pres, v3, v4, v5))

    return (now, temperatures[0][0], temperatures[1][0],
            temperatures[2][0], temperatures[3][0],
            ana_pres, prep_pres, v3, v4, v5)


def draw_graphs(data):
    """1st column が datetime オブジェクトの2Dデータを読み込んでグラフにする。"""
    for i in range(10):
        logger.debug('len(data[{}]) is {}'.format(i, data[i]))
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


adda = ADS1256()
adda.cal_self()
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
