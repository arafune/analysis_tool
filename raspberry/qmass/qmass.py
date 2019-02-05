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
#  logger.debug(bytes.fromhex('7e 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 2c 30 30 31 61 2c 32 3a 30 65 64 31'))


class Qmass():
    '''Qmass measurement system class'''
    def __init__(self, port='/dev/ttyUSB0'):
        '''Init Microvision plus'''
        self.ser = serial.Serial(port=port, baudrate=9600,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE)
        data_to_read = self.ser.in_waiting  # よけいなリードバッファがあった時用
        self.ser.read(data_to_read)
        #
        self.fil = 0  # 0: off, 1: Fil #1, 2: Fil #2
        self.multiplier = 0 # 0:off, 1:on
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
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            data_to_read = self.ser.in_waiting
        logger.debug(self.ser.read(data_to_read))  # aa d2
        self.ser.write(bytes.fromhex('ba 03'))
        self.ser.write(bytes.fromhex('a6'))
        self.ser.timeout = 0.2
        logger.debug(self.ser.readline())
        # 03 56 61 00 25 03 09 44 03 13 3e 02 2f 6a 03 00 00 01 00 4b 00
        self.ser.write(bytes.fromhex('bb 00 80 80 80 be 0a'))
        self.ser.write(bytes.fromhex('00 ff 00 bf 04'))
        logger.debug(self.ser.readline())
        # 8f 04 19 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 8e
        self.ser.write(bytes.fromhex('a7'))
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            time.sleep(1)
            data_to_read = self.ser.in_waiting
        logger.info(self.ser.read(data_to_read))  # ff 00
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
        end = self.ser.read(1)  #  0x86
        logger.debug('end')
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
        '''
        pass

    def set_start_mass(self, start_mass=4):
        '''Set start mass
        
        Parameters
        -----------
        start_mass: int
            start mass
        '''
        pass

    def set_mass_range(self, mass_range=0):
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
        pass

    def fil_off(self):
        '''Filament off
        '''
        pass
   
    def multiplier_on(self):
        '''multiplier on'''
        pass

    def multiplier_off(self):
        '''multiplier off'''
        pass
