#!/usr/bin/env python3
"""Modules for sensor set of multimonitor system.

Sensor set contains:
* 4ch MAX31856 Temperature multimonitor
* ADS1256 High precision ADC.
"""

import datetime
from logging import DEBUG, INFO, WARN, Formatter, StreamHandler, getLogger

import PiPyADC.pipyadc
from Adafruit_MAX31856 import max31856
from PiPyADC.ADS1256_definitions import *
from PiPyADC.pipyadc import ADS1256

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

# Input pin for the potentiometer on the Waveshare Precision ADC board:
EXT0 = POS_AIN0 | NEG_AINCOM
# Light dependant resistor of the same board:
EXT1 = POS_AIN1 | NEG_AINCOM
# The other external input screw terminals of the Waveshare board:
EXT2, EXT3 = POS_AIN2 | NEG_AINCOM, POS_AIN3 | NEG_AINCOM
EXT4, EXT5 = POS_AIN4 | NEG_AINCOM, POS_AIN5 | NEG_AINCOM
EXT6, EXT7 = POS_AIN6 | NEG_AINCOM, POS_AIN7 | NEG_AINCOM
# You can connect any pin as well to the positive as to the negative ADC input.
# The following reads the voltage of the potentiometer with negative polarity.
# The ADC reading should be identical to that of the POTI channel, but negative.
POTI_INVERTED = POS_AINCOM | NEG_AIN0
# For fun, connect both ADC inputs to the same physical input pin.
# The ADC should always read a value close to zero for this.
SHORT_CIRCUIT = POS_AIN0 | NEG_AIN0
# Specify here an arbitrary length list (tuple) of arbitrary input
# channel pair eight-bit code values to scan sequentially from index 0 to last.
# Eight channels fit on the screen nicely for this example..
CH_SEQUENCE = (EXT1, EXT2, EXT5, EXT6, EXT7)
#################################################################

adda = ADS1256()
adda.cal_self()
thermos = [
    max31856.MAX31856(software_spi={
        'clk': 25,
        'cs': 14,
        'do': 8,
        'di': 7
    }),
    max31856.MAX31856(software_spi={
        'clk': 25,
        'cs': 15,
        'do': 8,
        'di': 7
    }),
    max31856.MAX31856(software_spi={
        'clk': 25,
        'cs': 16,
        'do': 8,
        'di': 7
    }),
    max31856.MAX31856(software_spi={
        'clk': 25,
        'cs': 21,
        'do': 8,
        'di': 7
    })
]


def _pressure(volt):
    """Return the pressure (mbar) from the monitor voltage."""
    exponent = int(volt) - 11
    mantissa = (((volt - int(volt)) + .1) / .11) * 1.33322
    return mantissa * 10**exponent


def _read_temperatures():
    """Return temperatue data."""
    external = [thermos[i].read_temp_c() for i in range(4)]
    internal = [thermos[i].read_internal_temp_c() for i in range(4)]
    ret = []
    for i in range(4):
        ret.append((external[i], internal[i]))
    return ret


def read():
    """Read the values and save them."""
    raw_channels = adda.read_sequence(CH_SEQUENCE)
    # 1.004543 should be tuned.
    voltages = [(i * adda.v_per_digit) for i in raw_channels]
    temperatures = _read_temperatures()
    ana_pres = _pressure((voltages[0] + 0.000140) / 0.32354472361)
    prep_pres = _pressure((voltages[1] + 0.000140) / 0.32441316526)
    # calibrate by using ADVANTEST
    # ana_pres = pressure((voltages[0] + 0.000140) / 0.33467111)
    # prep_pres = pressure((voltages[1] + 0.000140) / 0.335202222)
    # port3 (voltage(port3) + 0.000140 ) / 0.335008777
    # port4 (voltage(port4) + 0.000140 ) / 0.334730222
    v3 = voltages[2]
    v4 = voltages[3]
    v5 = voltages[4]
    temp_fmt = 'Temperature at {}: {:6.3f} C (internal {:6.3f} C)'
    pressure_fmt = '{:.3e} mbar'
    voltage_fmt = '{:9.7f} V'
    for i in range(4):
        logger.info(temp_fmt.format(i, temperatures[i][0], temperatures[i][1]))
    logger.debug('Analysis corrected V: {:9.7f} V'.format(
        (voltages[0] + 0.000140) / 0.33467111))
    logger.debug('Preparation corrected V: {:9.7f} V'.format(
        (voltages[1] + 0.000140) / 0.335202222))
    logger.info('Analysis: ' + pressure_fmt.format(ana_pres))
    logger.info('Preparation: ' + pressure_fmt.format(prep_pres))
    logger.info('Voltage-3:' + voltage_fmt.format(v3))
    logger.info('Voltage-4:' + voltage_fmt.format(v4))
    logger.info('Voltage-5:' + voltage_fmt.format(v5))
    now = datetime.datetime.now()
    return (now, temperatures[0][0], temperatures[1][0], temperatures[2][0],
            temperatures[3][0], ana_pres, prep_pres, v3, v4, v5)


if __name__ == '__main__':
    readdata = read()
    print(readdata)
