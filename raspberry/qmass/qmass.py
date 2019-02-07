#!/usr/bin/env python3
'''Q-mass control by python
'''
import datetime
import time
from logging import getLogger, StreamHandler, DEBUG, Formatter
import serial

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

def pressure_indicator(pressure, pressure_pange):
    range_table = {0: 1E-7, 1: 1E-8, 2: 1E-9, 3:1E-10, 4:1E-11, 5: 1E-12, 6:1E-13}
    if isinstance(pressure_range, int):
        pressure_range = range_table[pressure_range]
    level = pressure/prassure_range
    if level > 1:
        level = 1
    level = int(level * 100)
    output = ''
    output = '.' * level
    output += '*'
    output += '.' * (100-level)
    return output

class Qmass():
    '''Qmass measurement system class

    Attributes
    ----------
    filament: int
        Acitive filament # (None for no-active filament)

    multiplier: Boolean
        True if multiplier is active

    start_mass: int
    mass_span: int
    accuracy:int
    pressure_range:int
    '''

    mass_span_analog = {0: 4, 1: 8, 2: 32, 3: 64}
    mass_span_digital = {0: 10, 1: 20, 2: 50, 3: 100, 4: 150, 5:200, 6:300}

    def __init__(self, port='/dev/ttyUSB0'):
        self.filament = None
        self.multiplier = False
        self.pressure_range = 0
        self.accuracy = 0
        self.start_mass = 0
        self.mass_span = 0
        self.com = serial.Serial(port=port, baudrate=9600, xonxoff=True,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE)

    def boot(self):
        '''Boot Microvision plus'''
        data_to_read = self.com.in_waiting  # よけいなリードバッファがあった時用
        self.com.read(data_to_read)
        #
        self.com.write(b'$$$$$$$$$$')
        self.com.write(b'{000D,10:1FB6')
        time.sleep(0.2)
        data_to_read = self.com.in_waiting
        while data_to_read == 0:
            data_to_read = self.com.in_waiting
        logger.info(self.com.read(data_to_read))
        # b'~LM76-00499001,001a,2:0ed1'
        self.com.write(b'}LM76-00499001,001A,5:1660')
        time.sleep(.2)
        data_to_read = self.com.in_waiting
        while data_to_read == 0:
            data_to_read = self.com.in_waiting
        logger.info(self.com.read(data_to_read))
        # b'~LM76-00499001,0025,3,1,V1.51a,0:262a'
        self.com.write(b'{0011,55,1,0:402A')
        time.sleep(.2)
        data_to_read = self.com.in_waiting
        while data_to_read == 0:
            data_to_read = self.com.in_waiting
        logger.info(self.com.read(data_to_read))
        # b'~LM76-00499001,001a,2:0ed1'
        self.com.write(b'}LM76-00499001,001B,15:A7C2')
        time.sleep(.2)
        data_to_read = self.com.in_waiting
        while data_to_read == 0:
            data_to_read = self.com.in_waiting
        logger.info(self.com.read(data_to_read))
        # b'~LM76-00499001,001c,6,0:daad'
        time.sleep(.1)   # << OK?
        self.com.write(bytes.fromhex('af'))
        # By commenting out the following line, "aa d2" can be read.
        # *But* cannot measure!!
        # time.sleep(2)
        self.com.write(bytes.fromhex('aa'))
        self.com.timeout = 0.3
        tmp = self.com.readline()
        logger.debug('should be "aa d2": {}'.format(tmp.hex()))
        tmp = self.com.reset_input_buffer()
        logger.debug('Return of reset_input_buffer: {}'.format(tmp))
        #time.sleep(1.5)   # << OK?
        self.com.write(bytes.fromhex('ba 03'))
        time.sleep(1.5)   # << OK?
        self.com.write(bytes.fromhex('a6'))
        data_to_read = self.com.in_waiting
        logger.debug('data_to_read: {}'.format(data_to_read))
        tmp = self.com.readline()
        logger.debug('035661...004b00: {}'.format(tmp))
        # 03 56 61 00 25 03 09 44 03 13 3e 02 2f 6a 03 00 00 01 00 4b 00
        self.com.write(bytes.fromhex('bb 00 80 80 80 be 0a'))
        self.com.write(bytes.fromhex('00 ff 00 bf 04'))
        tmp = self.com.readline()
        logger.debug('"8f041900...00008e": {}'.format(tmp.hex()))
        # 8f 04 19 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 8e
        self.com.write(bytes.fromhex('a7'))
        data_to_read = self.com.in_waiting
        logger.debug('data_to_read: {}'.format(data_to_read))
        tmp = self.com.readline()
        logger.debug('should be "ff 00": {}"'.format(tmp))
        self.com.write(bytes.fromhex('aa 01 03 10 86 00 a1 00 00 bc'))
        data_to_read = self.com.in_waiting
        while data_to_read == 0:
            data_to_read = self.com.in_waiting
        tmp = self.com.read(data_to_read)
        logger.debug('"#c2 52 85 7f": {}'.format(tmp))
        # c2 52 85 7f
        time.sleep(1)
        self.com.write(bytes.fromhex('ad 02'))
        tmp = self.com.readline()
        logger.debug('0x07: {}'.format(tmp))
        # 07
        self.com.write(bytes.fromhex('ad 03'))
        data_to_read = self.com.in_waiting
        while data_to_read == 0:
            data_to_read = self.com.in_waiting
        tmp = self.com.read(data_to_read)
        logger.debug('data_to_read is: {} & should be "1e": {}'.format(data_to_read, tmp))
        # 1e
        time.sleep(1)
        self.com.write(bytes.fromhex('e1 00'))
        data_to_read = self.com.in_waiting
        while data_to_read == 0:
            data_to_read = self.com.in_waiting
        tmp = self.com.read(data_to_read)
        logger.debug('"b2 33 8c bf": {}'.format(tmp))
        # b2 33 8c bf
        time.sleep(1)
        self.com.write(bytes.fromhex('bf 05'))
        tmp = self.com.readline()
        logger.debug('"8f 05 21 0d ... ff ff ff 8e": {}'.format(tmp))
        # 8f 05 21 0d 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 00 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff 8e
        self.com.write(bytes.fromhex('e6 80 00'))
        self.com.timeout = None
        logger.debug('Microvision initialized')
        time.sleep(1)

    def exit(self):
        '''Close Microvision plus'''
        self.com.write(b'\x00\xaf')
        end = self.com.read(1)  # 0x86
        logger.debug('End: should be 0x86 :{}'.format(end))
        self.com.write(b'\xe2')
        self.com.close()

    def set_accuracy(self, accuracy=0):
        '''set accuracy

        Parameters
        ----------
        accuracy: int
            default:0 ( 0 to 5)
        '''
        if accuracy == 0:
            self.com.write(b'\x22\x00')
        elif accuracy == 1:
            self.com.write(b'\x22\x01')
        elif accuracy == 2:
            self.com.write(b'\x22\x02')
        elif accuracy == 3:
            self.com.write(b'\x22\x03')
        elif accuracy == 4:
            self.com.write(b'\x22\x04')
        elif accuracy == 5:
            self.com.write(b'\x22\x05')
        else:
            raise ValueError("accuracy must be 0 - 5 and integer")

    def set_range(self, pressure_range=0):
        '''Set pressure range

        Parameters
        -----------
        pressure_range: int
            pressure range
            0: E-7
            1: E-8
            2: E-9
            3: E-10
            4: E-11
            5: E-12
            6: E-13
        '''
        if not self.multiplier:
            if pressure_range < 7:
                raise ValueError('=< E-11 when multiplier is off')
            pressure_range += 2
            command = '20 00 {:02} 00'.format(pressure_range)
        else:
            command = '20 02 {:02} 00'.format(pressure_range)
        self.com.write(bytes.fromhex(command))

    def analog_mode(self, start_mass=4, mass_span=2,
                    accuracy=5, pressure_range=4):
        '''Set analog Mode

        Parameters
        -----------
        star_mass: int
            default:4
        mass_span: int
            default: 2 (0:8, 1:16, 2:32, 3:64)
        accuracy: int
            default: 5
        pressure_range: int
            default 4: (E-11)
        '''
        self.pressure_range = pressure_range
        self.accuracy = accuracy
        self.start_mass = start_mass
        self.mass_span = mass_span
        command0 = '00 e4 00 00 02 01 '
        if self.multiplier:
            command_pressure = '02 {:02} '.format(pressure_range)
        else:
            command_pressure = '00 {:02} '.format(pressure_range-2)
        command_accuracy = '00 {:02} '.format(accuracy)
        command_mass_span = '{:02} '.format(mass_span)
        command_start_mass = '00 {:02} 00 '.format(start_mass-1)
        command = command0 + command_pressure + command_accuracy
        command += command_mass_span + command_start_mass
        logger.debug('command: {}'.format(command))
        self.com.write(bytes.fromhex(command))
        return 0

    def digital_mode(self, start_mass=4, mass_span=2,
                     accuracy=5, pressure_range=4):
        '''Set Digital mode

        Parameters
        -----------
        star_mass: int
            default:4
        mass_span: int
            default: 2 (0:8, 1:16, 2:32, 3:64)
        accuracy: int
            default: 5
        pressure_range: int
            default 4: (E-11)
        '''
        self.pressure_range = pressure_range
        self.accuracy = accuracy
        self.start_mass = start_mass
        self.mass_span = mass_span
        command0 = '00 e4 00 00 02 02 '
        if self.multiplier:
            command_pressure = '02 {:02x} '.format(pressure_range)
        else:
            command_pressure = '00 {:02x} '.format(pressure_range - 1)
        command_accuracy = '00 {:02x} '.format(accuracy)
        command_start_mass = '00 {:02x} '.format(start_mass - 1)
        end_mass = start_mass + Qmass.mass_span_digital[mass_span] - 1
        command_end_mass = '{:04x} '.format(end_mass)
        command_mass_span = '{:02x} ff'.format(mass_span)  # << end with 'ff' or '00'?
        command = command0 + command_pressure + command_accuracy
        command += command_mass_span + command_start_mass
        command += command_mass_span
        logger.debug('command: {}'.format(command))
        self.com.write(bytes.fromhex(command))
        return 1

    def leak_check(self, mass=4, accuracy=5, pressure_range=4):
        '''Set Leak check mode

        Mass offset canbe set. But not supported yet.

        Parameters
        -----------
        mass: int
            default:4
        accuracy: int
            default: 5
        pressure_range: int
            default 4: (E-11)
        '''
        command0 = '00 e4 00 00 02 04 '
        if self.multiplier:
            command_pressure = '02 {:02x} '.format(pressure_range)
        else:
            command_pressure = '00 {:02x} '.format(pressure_range - 1)
        command_accuracy = '{:02x}'.format(accuracy)
        command_mass = '{:04x} 10 01'.format(mass) 
        command = command0 + command_pressure + command_accuracy
        command += command_mass
        logger.debug('command: {}'.format(command))
        self.com.write(bytes.fromhex(command))
        return 2

    def measure(self, mode=0, start_mass=4,
                mass_span=2, accuracy=5, pressure_range=4):
        '''measurement

        Parameters
        ----------

        mode: int
            mode type
            0: Analog mode
            1: Digital mode
            2: Leak check mode
        '''
        scan_start = bytes.fromhex('b6')
        self.com.write(scan_start)
        if mode == 0:
           mass_step = 1/(256/Qmass.mass_span_analog[mass_span])
           mass = start_mass - (
               (256/Qmass.mass_span_analog[mass_span])/2 - 1) * mass_step
           logger.debug('mass:{} mass_step: {}'.format(mass, mass_step))
        else:
            mass_step = 1
            mass = start_mass
        try:
            while True:
                data_bytes = self.com.read(3)
                if data_bytes[0] == 0x7f:
                    pressure = 0.0
                else:
                    pressure = data_bytes[1] * 1.216 + (data_bytes[2] - 64) * 0.019
                if b'\xf0' in data_bytes:   # 0xf0 0xf0 0xf4 (analog), 0xf0 0xf0 0xf1 (digital)
                    logger.debug('data_bytes is: {}'.format(data_bytes))
                    time.sleep(0.5)
                    self.com.reset_input_buffer()
                    self.com.write(scan_start)
                    if mode == 0:
                        mass = start_mass - (
                            (256 / Qmass.mass_span_analog[mass_span])
                            / 2 - 1) * mass_step
                    else:
                        mass = start_mass
                    logger.debug('Rescan')
                else:
                    if mode < 2:
                        fmt = 'byte code: {:02x} {:02x} {:02x}, Pressure: {:4f} / {}'
                        logger.debug(fmt.format(data_bytes[0], data_bytes[1], data_bytes[2],
                                                pressure, mass))
                        mass += mass_step
                    else:
                        print('Pressure:{:4f}: {}'.format(pressure,
                                                          pressure_indicator(pressure, pressure_range)))
        except KeyboardInterrupt:
            self.com.write(bytes.fromhex('00 00'))
            time.sleep(1)


    def set_start_mass(self, start_mass=4):
        '''Set start mass

        Parameters
        -----------
        start_mass: int
            start mass
        '''
        command = '23 {:02} 00'.format(start_mass-1)
        self.com.write(bytes.fromhex(command))

    def set_mass_span(self, mass_span=0):
        '''Set mass range

        Parameters
        -----------
        mass_range: int
            mass range: 0: 4, 1:  , 2:  , 3:  4:...

        '''
        pass

    def fil_on(self, fil_no=1):
        '''Filament on
        '''
        if not self.filament:
            if fil_no == 1:
                self.com.write(b'\xe3\x48')
                self.filament = 1
                logger.debug('Filament #1 on')
            elif fil_no == 2:
                self.com.write(b'\xe3\x50')   # << check!!
                self.filament = 2
                logger.debug('Filament #2 on')
        elif self.filament == 1 and fil_no == 2:
            self.fil_off()
            self.com.write(b'\xe3\x50')
            self.filament = 2
            logger.debug('Filament #2 on')
        elif self.filament == 2 and fil_no == 1:
            self.fil_off()
            self.com.write(b'\xe3\x48')
            self.filament = 1
            logger.debug('Filament #1 on')
        else:
            raise ValueError

    def fil_off(self):
        '''Filament off
        '''
        self.com.write(b'\xe3\x40')
        tmp = self.com.read(1)
        logger.debug('Filament off: {}'.format(tmp))
        self.filament = False

    def multiplier_on(self):
        '''multiplier on'''
        self.com.write(b'\x20\x02\x00')
        logger.debug('Multiplier ON')
        self.multiplier = True

    def multiplier_off(self):
        '''multiplier off'''
        self.com.write(b'\x20\x00\x00')
        time.sleep(.5)
        data_to_read = self.com.in_waiting
        tmp = self.com.read(data_to_read)
        logger.debug('Multiplier off'.format(tmp))
        self.multiplier = False


if __name__ == '__main__':
    start_mass = 4
    mass_span = 3
    accuracy = 5
    pressure_range = 5
    port = '/dev/ttyUSB1'
    q_mass = Qmass(port=port)
    q_mass.boot()
    q_mass.fil_on(1)
    q_mass.multiplier_on()
    q_mass.analog_mode(start_mass=start_mass, mass_span=mass_span,
                       accuracy=accuracy, pressure_range=pressure_range)
    q_mass.measure(mode=0, start_mass=start_mass, mass_span=mass_span,
                   accuracy=accuracy, pressure_range=pressure_range)
    q_mass.multiplier_off()
    q_mass.fil_off()
    q_mass.exit()
