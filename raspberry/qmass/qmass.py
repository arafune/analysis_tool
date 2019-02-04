#!/usr/bin/env python3
'''Q-mass control by python
'''
import serial


class Qmass():
    '''Qmass measurement system class'''
    def __init__(self, port='/dev/ttfUSB0'):
        '''Init Microvision plus'''
        self.ser = serial.Serial(port=port, baudrate=9600,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE)
        data_to_read = self.ser.in_waiting  # よけいなリードバッファがあった時用
        self.ser.read(data_to_read)
        #
        self.fil = 0  # 0: 0ff, 1: Fil #1, 2: Fil #2
        #
        self.ser.write(b'$$$$$$$$$$')
        self.ser.write(bytes.fromhex('7b 30 30 30 44 2c 31 30 3a 31 46 42 36'))
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            data_to_read = self.ser.in_waiting
        ret1 = self.ser.read(data_to_read)
        self.ser.write(bytes.fromhex('7d 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 2c 30 30 31 41 2c 35 3a 31 36 36 30'))
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            data_to_read = self.ser.in_waiting
        ret2 = self.ser.read(data_to_read)
        self.ser.write(bytes.fromhex('7b 30 30 31 31 2c 35 35 2c 31 2c 30 3a 34 30 32 41'))
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            data_to_read = self.ser.in_waiting
        ret3 = self.ser.read(data_to_read)
        self.ser.write(bytes.fromhex('7d 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 2c 30 30 31 42 2c 31 35 3a 41 37 43 32'))
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            data_to_read = self.ser.in_waiting
        ret4 = self.ser.read(data_to_read)
        print(ret1)
        print(ret2)
        print(ret3)
        print(ret4)
        self.ser.write(bytes.fromhex('af'))
        self.ser.write(bytes.fromhex('aa'))
        data_to_read = self.ser.in_waiting
        while data_to_read == 0:
            data_to_read = self.ser.in_waiting
        ret5 = self.ser.read(data_to_read)  # aa d2
        self.ser.write(bytes.fromhex('ba 03 a6'))
        '''
        PC:[Mon Feb  4 14:36:20 2019] 24 24 24 24 24 24 24 24 24 24
        PC:[Mon Feb  4 14:36:20 2019] 7b 30 30 30 44 2c 31 30 3a 31 46 42 36
        DEVICE:[Mon Feb  4 14:36:21 2019] 7e 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 2c 30 30 31 61 2c 32 3a 30 65 64 31
        PC:[Mon Feb  4 14:36:21 2019] 7d 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 2c 30 30 31 41 2c 35 3a 31 36 36 30
        DEVICE:[Mon Feb  4 14:36:21 2019] 7e 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 2c 30 30 32 35 2c 33 2c 31 2c 56 31 2e 35 31 61 2c 30 3a 32 36 32 61
        PC:[Mon Feb  4 14:36:21 2019] 7b 30 30 31 31 2c 35 35 2c 31 2c 30 3a 34 30 32 41
        DEVICE:[Mon Feb  4 14:36:22 2019] 7e 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 2c 30 30 31 61 2c 32 3a 30 65 64 31
        PC:[Mon Feb  4 14:36:22 2019] 7d 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 2c 30 30 31 42 2c 31 35 3a 41 37 43 32
        DEVICE:[Mon Feb  4 14:36:22 2019] 7e 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 2c 30 30 31 63 2c 36 2c 30 3a 64 61 61 64
        PC:[Mon Feb  4 14:36:22 2019] af
        PC:[Mon Feb  4 14:36:26 2019] aa
        DEVICE:[Mon Feb  4 14:36:26 2019] aa d2
        PC:[Mon Feb  4 14:36:26 2019] ba 03
        PC:[Mon Feb  4 14:36:27 2019] a6
        DEVICE:[Mon Feb  4 14:36:27 2019] 03 56 61 00 25 03 09 44 03 13 3e 02 2f 6a 03 00 00 01 00 4b 00
        PC:[Mon Feb  4 14:36:27 2019] bb 00 80 80 80 be 0a
        PC:[Mon Feb  4 14:36:28 2019] 00 ff 00 bf 04
        DEVICE:[Mon Feb  4 14:36:28 2019] 8f 04 19 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 8e
        PC:[Mon Feb  4 14:36:28 2019] a7
        DEVICE:[Mon Feb  4 14:36:28 2019] ff 00
        PC:[Mon Feb  4 14:36:28 2019] aa 01 03 10 86 00 a1 00 00 bc
        DEVICE:[Mon Feb  4 14:36:28 2019] c2 52 85 7f
        PC:[Mon Feb  4 14:36:28 2019] ad 02
        DEVICE:[Mon Feb  4 14:36:29 2019] 07
        PC:[Mon Feb  4 14:36:29 2019] ad 03
        DEVICE:[Mon Feb  4 14:36:29 2019] 1e
        PC:[Mon Feb  4 14:36:29 2019] e1 00
        DEVICE:[Mon Feb  4 14:36:29 2019] b2 33 8c bf
        PC:[Mon Feb  4 14:36:29 2019] bf 05
        DEVICE:[Mon Feb  4 14:36:29 2019] 8f 05 21 0d 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 00 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff 8e
        PC:[Mon Feb  4 14:36:29 2019] e6 80
        PC:[Mon Feb  4 14:36:30 2019] 00
'''

    def exit(self):
        '''Close Microvision plus'''
        self.ser.write(b'\x00\xaf')
        self.ser.read(1)  #  0x86
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
