#! /usr/bin/env python
import serial    # pyserial
import datetime
 
 
def to_hex(input_str):
    outpur_str = " ".join("{:02x}".format(ord(c)) for c in input_str)
    # 4b 41 20 30 20 46 46 0d
    return outpur_str
 
 
def main():
    ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    xonxoff=True,
    )
    # open if not opened
    if ser.isOpen() == False:
        print "OPENING port."
        ser.open()
    # header
    fmt = "{0:15}{1:35}{2}"
    print fmt.format('TIME', 'RAW HEX', 'TIME DELTA')
    # so to have first value
    time_of_last_read = datetime.datetime.now()
    while True:
        data_to_read = ser.in_waiting
        if data_to_read != 0: # read if tehre is new data
            time_now = datetime.datetime.now()   
            data = ser.read(data_to_read)
            hex_with_space = to_hex(data)
            time_with_miliseconds = time_now.strftime("%H:%M:%S.%f")[:-3]
            time_delta = time_now - time_of_last_read
            print fmt.format(time_with_miliseconds, hex_with_space, time_delta)
            # last time
            time_of_last_read = time_now
    ser.close()


if __name__ == '__main__':
    main()
