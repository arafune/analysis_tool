#!/usr/bin/env python3
'''Q-mass control by python
'''
import time
from logging import getLogger, StreamHandler, DEBUG
import serial

# logger
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


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

    def __init__(self, port='/dev/ttyUSB0'):
        self.filament = None
        self.multiplier = False
        self.pressure_range = 0
        self.accuracy = 0
        self.start_mass = 0
        self.mass_span = 0
        self.boot(port)

    def boot(self, port='/dev/ttyUSB0'):
        '''Boot Microvision plus'''
        self.ser = serial.Serial(port=port, baudrate=9600, xonxoff=True,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE)
        data_to_read = self.ser.in_waiting  # よけいなリードバッファがあった時用
        self.ser.read(data_to_read)
        #
        self.ser.write(b'$$$$$$$$$$')
        self.ser.write(b'{000D,10:1FB6')
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            time.sleep(0.1)
            data_to_read = self.ser.in_waiting
        logger.info(self.ser.read(data_to_read))
        # b'~LM76-00499001,001a,2:0ed1'
        self.ser.write(b'}LM76-00499001,001A,5:1660')
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            time.sleep(0.1)
            data_to_read = self.ser.in_waiting
        logger.info(self.ser.read(data_to_read))
        # b'~LM76-00499001,0025,3,1,V1.51a,0:262a'
        self.ser.write(b'{0011,55,1,0:402A')
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            time.sleep(0.1)
            data_to_read = self.ser.in_waiting
        logger.info(self.ser.read(data_to_read))
        # b'~LM76-00499001,001a,2:0ed1'
        self.ser.write(b'}LM76-00499001,001B,15:A7C2')
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            time.sleep(0.1)
            data_to_read = self.ser.in_waiting
        logger.info(self.ser.read(data_to_read))
        # b'~LM76-00499001,001c,6,0:daad'
        self.ser.write(bytes.fromhex('af'))
        self.ser.write(bytes.fromhex('aa'))
        self.ser.timeout = 0.2
        tmp = self.ser.readline()
        logger.debug('should be "aa d2" {}'.format(tmp))
        # aa d2
        self.ser.write(bytes.fromhex('ba 03'))
        self.ser.write(bytes.fromhex('a6'))
        tmp = self.ser.readline()
        logger.debug(tmp)
        # 03 56 61 00 25 03 09 44 03 13 3e 02 2f 6a 03 00 00 01 00 4b 00
        self.ser.write(bytes.fromhex('bb 00 80 80 80 be 0a'))
        self.ser.write(bytes.fromhex('00 ff 00 bf 04'))
        logger.debug(self.ser.readline())
        # 8f 04 19 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 8e
        self.ser.write(bytes.fromhex('a7'))
        data_to_read = self.ser.in_waiting
        logger.info('should be "ff 00"  {}"'.format(self.ser.read(2)))  # ff 00
        self.ser.write(bytes.fromhex('aa 01 03 10 86 00 a1 00 00 bc'))
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            data_to_read = self.ser.in_waiting
        logger.debug(self.ser.read(data_to_read))
        # c2 52 85 7f
        self.ser.write(bytes.fromhex('ad 02'))
        logger.debug(self.ser.readline())
        # 07
        self.ser.write(bytes.fromhex('ad 03'))
        time.sleep(1)
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            data_to_read = self.ser.in_waiting
        logger.debug(self.ser.read(data_to_read))
        # 1e
        self.ser.write(bytes.fromhex('e1 00'))
        time.sleep(1)
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            data_to_read = self.ser.in_waiting
        logger.debug(self.ser.read(data_to_read))
        # b2 33 8c bf
        self.ser.write(bytes.fromhex('bf 05'))
        data_to_read = self.ser.in_waiting
        logger.debug('data_to_read : {}'.format(data_to_read))
        logger.debug(self.ser.readline())
        # 8f 05 21 0d 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 00 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff 8e
        self.ser.write(bytes.fromhex('e6 80 00'))
        self.ser.timeout = None
        logger.debug('Microvision initialized')

    def exit(self):
        '''Close Microvision plus'''
        self.ser.write(b'\x00\xaf')
        end = self.ser.read(1)  # 0x86
        logger.debug('End: should be 0x86 {}'.format(end))
        self.ser.write(b'\xe2')

    def set_accuracy(self, accuracy=0):
        '''set accuracy

        Parameters
        ----------
        accuracy: int
            default:0 ( 0 to 5)
        '''
        if accuracy == 0:
            self.ser.write(b'\x22\00')
        elif accuracy == 1:
            self.ser.write(b'\x22\01')
        elif accuracy == 2:
            self.ser.write(b'\x22\02')
        elif accuracy == 3:
            self.ser.write(b'\x22\03')
        elif accuracy == 4:
            self.ser.write(b'\x22\04')
        elif accuracy == 5:
            self.ser.write(b'\x22\05')
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
        self.ser.write(bytes.fromhex(command))

    def analog_mode(self, start_mass=4, mass_span=2,
                    accuracy=5, pressure_range=4):
        '''Run analog Mode

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
            command_pressure = '02 {:02}'.format(pressure_range)
        else:
            command_pressure = '00 {:02}'.format(pressure_range-1)
        command_accuracy = '00 {:02} '.format(accuracy)
        command_mass_span = '{:02} '.format(mass_span)
        command_start_mass = '00 {:02} 00 '.format(start_mass-1)
        command = command0 + command_pressure + command_accuracy
        command += command_mass_span + command_start_mass
        self.ser.write(bytes.fromhex(command))

    def measure(self):
        '''measurement'''
        scan_start = bytes.fromhex('b6')
        self.ser.write(scan_start)
        while True:
            data_bytes = self.ser.read(3)
            if data_bytes[0] == b'\x7f':
                pressure = 0
            else:
                pressure = data_bytes[1] * 1.22 + (data_bytes[2] - 64) * 0.019 logger.debug('Pressure is {:4f}'.format(pressure))
            if data_bytes == b'\x0f0 \xf0 \xf4':
                self.ser.write(scan_start)
                logger.debug('Backto start mass')

    def set_start_mass(self, start_mass=4):
        '''Set start mass

        Parameters
        -----------
        start_mass: int
            start mass
        '''
        pass
        command = '23 {:02} 00'.format(start_mass-1)
        self.ser.write(bytes.fromhex(command))

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
                self.ser.write(b'\xe3\x48')
                self.filament = 1
            elif fil_no == 2:
                self.ser.write(b'\xe3\x50')   # << check!!
                self.filament = 2
        elif self.filament == 1 and fil_no == 2:
            self.fil_off()
            self.ser.write(b'\xe3\x50')
            self.filament = 2
        elif self.filament == 2 and fil_no == 1:
            self.fil_off()
            self.ser.write(b'\xe3\x48')
            self.filament = 1
        else:
            raise ValueError

    def fil_off(self):
        '''Filament off
        '''
        self.ser.write(b'\xe3\x40')
        self.filament = False

    def multiplier_on(self):
        '''multiplier on'''
        self.ser.write(b'\x20\x02\x00')
        self.multiplier = True

    def multiplier_off(self):
        '''multiplier off'''
        self.ser.write(b'\x20\x00\x00')
        self.multiplier = False


if __name__ == '__main__':
    q_mass = Qmass('/dev/ttyUSB1')
    time.sleep(1)
    q_mass.fil_on(1)
    q_mass.multiplier_on()
    q_mass.analog_mode(start_mass=4, mass_span=2, accuracy=5, pressure_range=4)
    try:
       q_mass.measure()
    except KeyboardInterrupt:
        q_mass.multiplier_off()
        q_mass.fil_off()
        q_mass.exit()


