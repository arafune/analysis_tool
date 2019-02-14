#!/usr/bin/env python3
"""Manipulator (Z, and phi) module."""
import argparse

import serial


class QTADM2():
    """Manipulator motor control."""

    #  0 counts indicates:
    INITZ = 0  # mm
    INIT_THETA = 0  # degree
    #  unit movement
    ONE_MM = 6000  # pulse/mm
    ONE_DEG = 1200  # pulse/deg
    #
    UPPER_Z = 75  # mm
    LOWER_Z = 25  # mm
    #
    TRANSFER_ANGLE = 270  # deg
    MEASUREMENT_ANGLE = 315  # deg

    #
    def __init__(self, port='/dev/ttyUSB0'):
        """Initialization."""
        # com のセット
        # スピードセット？
        self.com = serial.Serial(port=port)
        self.com.write(b'D:A500P10000P100\r\n')
        self.com.write(b'D:B500P9000P100\r\n')
        self.com.write(b'F:\r\n')
        _ok = self.com.readline()
        if _ok.decode('utf-8').strip() == 'OK':
            return
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
        if 0 <= pos_mm <= 100:
            move_pulse = int(pos_mm / QTADM2.ONE_MM)
            command = 'AGO:B{}\r\n'.format(move_pulse)
            self.com.write(command.encode('utf-8'))
        else:
            raise ValueError('Z position must be 0 to 100')

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
            raise ValueError('Angle must be -180 to 360 deg')
        command = 'AGO:A{}\r\n'.format(pulse)
        self.com.write(command.encode('uft-8'))

    def rotate_move(self, angle_deg, pos_mm):
        """Rotate and then vertically move.

        Parameters
        -----------
        angle_deg: float
            Angle
        pos_mm: float
            position
        """
        if 0 <= pos_mm <= 100:
            move_pulse = int(pos_mm / QTADM2.ONE_MM)
            if 0 <= angle_deg <= 180:
                angle_pulse = int(angle_deg * QTADM2.ONE_DEG)
            elif (180 < angle_deg < 360) or (-180 < angle_deg < 0):
                angle_pulse = int(-angle_deg * QTADM2.ONE_DEG)
            else:
                raise ValueError('Angle must be -180 to 360 deg')
        else:
            raise ValueError('Z position must be 0 to 100')
        command = 'AGO:A{}B{}\r\n'.format(angle_pulse, move_pulse)
        self.com.write(command.encode('uft-8'))

    def move_by(self, z_mm):
        """Relative move by milimeter."""
        current_z = self.current_position(physical=True)[1]
        if z_mm + current_z < 0 or z_mm + current_z > 100:
            raise ValueError('Value check. Do nothing.')
        pulse = int(z_mm * QTADM2.ONE_MM)
        command = 'MGO:B{}'.format(pulse)
        self.com.write(command.encode('utf-8'))

    def rotate_by(self, deg):
        """Relative rotate by degree."""
        current_angle = self.current_position(physical=True)[0]
        if -180 < current_angle + deg < 360:
            print('Value check. Do nothing')
            return
        pulse = int(deg * QTADM2.ONE_DEG)
        command = 'MGO:A{}'.format(pulse)
        self.com.write(command.encode('utf-8'))

    def close(self):
        """Close RS232C port."""
        self.com.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--measurement',
        '-m',
        help="""Measurement position
    U or A: Upper sample is measured.
    D or B: Lower sample is measured.
    """)
    group.add_argument(
        '--transfer',
        '-t',
        help="""Transfer position
    U or A: Upper sample is measured.
    D or B: Lower sample is measured.
    """)
    args = parser.parse_args()
    while True:
        inp = input('Check the door close. OK? (yes) >>')
        if inp in ('yes', 'ok'):
            break
    if args.transfer:
        qtadm2 = QTADM2()
        u_or_d = args.transfer.upper()
        if u_or_d in ('U', 'A'):
            qtadm2.rotate_move(
                angle_deg=QTADM2.TRANSFER_ANGLE, pos_mm=QTADM2.UPPER_Z)
        elif u_or_d in ('D', 'B'):
            qtadm2.rotate_move(
                angle_deg=QTADM2.TRANSFER_ANGLE, pos_mm=QTADM2.LOWER_Z)
        else:
            qtadm2.close()
            raise RuntimeError('Set U or D')
    if args.measure:
        qtadm2 = QTADM2()
        u_or_d = args.measure.upper()
        if u_or_d in ('U', 'A'):
            qtadm2.rotate_move(
                angle_deg=QTADM2.MEASUREMENT_ANGLE, pos_mm=QTADM2.UPPER_Z)
        elif u_or_d in ('D', 'B'):
            qtadm2.rotate_move(
                angle_deg=QTADM2.MEASUREMENT_ANGLE, pos_mm=QTADM2.LOWER_Z)
        else:
            qtadm2.close()
            raise RuntimeError('Set U or D')
    qtadm2.close()
