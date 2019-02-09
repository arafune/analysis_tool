#!/usr/bin/env python3
'''Multi channel (7 ch for Voltage, 4 ch for temperature)'''

import time
import datetime
import HPADDA
from Adafruit_MAX31856 import max31856


def pressure(volt):
    '''Return the pressure (mbar) from the monitor voltage'''
    pass

adda = HPADDA.Board()
adda.set_sample_rate(300)
THERMOCOUPLES = [max31856.MAX31856(software_spi={'clk':25, 'cs':14, 'do':8, 'di':7}),
                 max31856.MAX31856(software_spi={'clk':25, 'cs':15, 'do':8, 'di':7}),
                 max31856.MAX31856(software_spi={'clk':25, 'cs':16, 'do':8, 'di':7}),
                 max31856.MAX31856(software_spi={'clk':25, 'cs':21, 'do':8, 'di':7})]



def single_read():
    #voltages = [ adda.get_voltage(ch) for ch in range(8) ]
    voltages =adda.get_voltage(6)
    temperatures = [THERMOCOUPLES[i].read_temp_c() for i in range(4)]
    print ('{:.4e}'.format(voltages))
    print(temperatures)

while True:
    single_read()
