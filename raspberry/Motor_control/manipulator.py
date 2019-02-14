#!/usr/bin/env python3
"""Manipulator (Z, and phi) module."""
import argparse
import serial


class QTADM2():
    """Manipulator motor control."""

    #  0 counts indicates:
    INITZ = 0          # mm
    INIT_THETA = 0   # degree
    #  unit movement
    ONE_MM = 6000     # pulse/mm
    ONE_DEG = 1200    # pulse/deg

    def __init__(self):
        """Initialization."""
        # com のセット
        # スピードセット？
        self.com = serial.Serial(port='/dev/ttyUSB0')
        self.com.write(b'D:A500P10000P100\r\n')
        self.com.write(b'D:B500P9000P100\r\n')
        self.com.write(b'F:\r\n')
        ok = self.readline()
        if ok.decode('utf-8').strip() == 'OK':
            return
        else:
            raise RuntimeError

    def current_position(self, physical=False):
        """Return current position.

        Parameters
        ----------
        phyiscs: Boolean
            if True, return position by physical unit(mm, degree)
            not count (defalut:False)

        """
        self.com.write('bQ:0\r\n')
        positions = self.com.readline().strip().split(',')
        positions = tuple([int(i) for i in positions])
        if physical:
            theta = positions[0]
            theta = 270 + theta / QTADM2.ONE_DEG
            pos_z = positions[1]
            pos_z = pos_z / QTADM2.ONE_MM
            return (theta, pos_z)
        return positions

    def move_to(self, pos_mm):
        """Move to position Z.

        Parameters
        -------------
        pos_mm: float
                position

        """
        move_pulse = int(pos_mm / QTADM2.ONE_MM)
        command = 'AGO:B{}\r\n'.format(move_pulse)
        self.com.write(command.encode('utf-8'))

    def rotate_to(self, angle_deg):
        """Rotate to angle theta.

        Parameters
        ------------
        angle_deg: float
            Angle.

        """
        if 0 <= angle_deg <= 180:
            pulse = int(angle_deg * QTADM2.ONE_DEG)
        elif (180 < angle_deg < 360) or (-180 < angle_deg < 0):
            pulse = int(-angle_deg * QTADM2.ONE_DEG)
        else:
            raise ValueError
        command = 'AGO:A{}\r\n'.format(pulse)
        self.com.write(command.encode('uft-8'))

    def move_by(self, z_mm):
        """Relative move by milimeter."""
        pulse = int(z_mm * QTADM2.ONE_MM)
        command = 'MGO:B{}'.format(pulse)
        self.com.write(command.encode('utf-8'))

    def rotate_by(self, deg):
        """Relative rotate by degree."""
        pulse = int(deg * QTADM2.ONE_DEG)
        command = 'MGO:A{}'.format(pulse)
        self.com.write(command.encode('utf-8'))

    def close(self):
        """Close RS232C port."""
        self.com.close()


if __name__ == '__main__':
    pass
