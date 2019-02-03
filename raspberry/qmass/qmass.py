#!/usr/bin/env python3
'''Q-mass control by python
'''
import serial

PORT = '/dev/ttyUSB0'

class Qmass():
    '''Qmass measurement system class'''
    def __init__(self):
        '''Init Microvision'''
        self.ser = serial.Serial(port=PORT, baudrate=9600,
                parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        data_to_read = ser.in_waiting  # よけいなリードバッファがあった時用
        self.read(data_to_read)
        #
        self.write(b'$$$$$$$$$$')
        self.write(bytes.fromhex('7b 30 30 30 44 2c 31 30 3a 31 46 42 36'))
        data_to_read = ser.in_waiting
        while data_to_read == 0:
            data_to_read = ser.in_waiting
        ret1 = ser.read(data_to_read)
        self.write(bytes.fromhex('7d 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 2c 30 30 31 41 2c 35 3a 31 36 36 30'))
        data_to_read = ser.in_waiting
        while data_to_read == 0:
            data_to_read = ser.in_waiting
        ret2 = ser.read(data_to_read)
        self.write(bytes.fromhex('7b 30 30 31 31 2c 35 35 2c 31 2c 30 3a 34 30 32 41'))
        data_to_read = ser.in_waiting
        while data_to_read == 0:
            data_to_read = ser.in_waiting
        ret3 = ser.read(data_to_read)
        self.write(bytes.fromhex('7d 4c 4d 37 36 2d 30 30 34 39 39 30 30 31 2c 30 30 31 42 2c 31 35 3a 41 37 43 32'))
        data_to_read = ser.in_waiting
        while data_to_read == 0:
            data_to_read = ser.in_waiting
        ret4 = ser.read(data_to_read)
        print(ret1)
        print(ret2)
        print(ret3)
        print(ret4)

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



