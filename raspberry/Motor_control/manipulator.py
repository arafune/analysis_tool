#!/usr/bin/env python3
'''
Manipulator (Z, and phi) 用 module
'''

class QTADM2():
    """Manipulator motor control."""

    def __init__():
    """Initialization.""" 
    # com のセット
    # スピードセット？
    



    def move_to(self, pos_mm):
        """move along Z.
       
        Parameters
        -------------
        pos_mm: float
                position
                
        memo 600000pulse = 10cm"""


    def rotate_to(self, angle_deg):
        """Rotate theta.


        Parameters
        ------------
        angle_deg: float
            Angle.
        memo: 54000pulse= 45degree"""

def init():
    '''Initialization'''
    pass


def set_zero():
    '''Set current position 'zero' '''
    pass


def move_to_zero():
    '''move to zero position'''
    pass


def move_abs(pos_mm):
    '''move absolute position'''
    pass


def move_ref(move_mm):
    '''move relatively'''
    pass


def set_zero_deg():
    '''Set current position 'zero' degree'''
    pass


def rotate_to_zero_deg():
    '''move to zero position'''
    pass


def rotate_abs_deg(pos_deg):
    '''move absolute position'''
    pass


def rotate_ref_deg(move_deg):
    '''move relatively'''
    pass


if __name__ == '__main__':
    pass
