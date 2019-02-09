#!/usr/bin/env python3
'''Multi channel (7 ch for Voltage, 4 ch for temperature)'''

from time import sleep
import datetime
from logging import getLogger, StreamHandler, DEBUG, Formatter
import HPADDA
from Adafruit_MAX31856 import max31856

# logger
logger = getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
formatter = Formatter(fmt)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False

def pressure(volt):
    '''Return the pressure (mbar) from the monitor voltage'''
    exponent = int(volt) - 11
    mantissa = ((volt - int(volt)) + .1)/.11
    return mantissa * 10**exponent

adda = HPADDA.Board()
adda.set_sample_rate(300)
THERMOCOUPLES = [max31856.MAX31856(software_spi={'clk':25, 'cs':14,
                                                 'do':8, 'di':7}),
                 max31856.MAX31856(software_spi={'clk':25, 'cs':15,
                                                 'do':8, 'di':7}),
                 max31856.MAX31856(software_spi={'clk':25, 'cs':16,
                                                 'do':8, 'di':7}),
                 max31856.MAX31856(software_spi={'clk':25, 'cs':21,
                                                 'do':8, 'di':7})]


def read_temperatures():
    '''Return temperatue data.

    '''
    external = [THERMOCOUPLES[i].read_temp_c() for i in range(4)]
    internal = [THERMOCOUPLES[i].read_internal_temp_c() for i in range(4)]
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
    voltage = adda.get_voltage(chamber+1)
    return pressure(voltage)

LOGFILE = open('log.txt', mode='w')
SAVE_FMT = '{} {:6.3f}\t{:6.3f}\t{:6.3f}\t{:6.3f}'
SAVE_FMT += '\t{:.3e}\t{:.3e}\t{:6.3f}\t{:6.3f}\t{:6.3f}'

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
        logger.debug(temp_fmt.format(i,
                                     temperatures[i][0],
                                     temperatures[i][1]))
    logger.debug('Analysis: ' + pressure_fmt.format(ana_pres))
    logger.debug('Preparation: ' + pressure_fmt.format(prep_pres))
    logger.debug('Voltage-3:' + voltage_fmt.format(v3))
    logger.debug('Voltage-4:' + voltage_fmt.format(v4))
    logger.debug('Voltage-5:' + voltage_fmt.format(v5))
    now = datetime.datetime.strftime(datetime.datetime.now(),
                                     '%Y-%m-%d %H:%M:%S')
    LOGFILE.write(SAVE_FMT.format(now,
                                  temperatures[0][0], temperatures[1][0],
                                  temperatures[2][0], temperatures[3][0],
                                  ana_pres, prep_pres, v3, v4, v5))

try:
    while True:
        read_and_save()
        sleep(1)
except KeyboardInterrupt:
    LOGFILE.close()
