#!/usr/bin/env python3
'''
Delay line 用 module
'''

import time
import Gpib


class FC104():
    """Class for Linear Translation feedback stage controller."""
    DEFAULT_POSITION = 0.0

    def __init__(self):
        """Initialization."""
        self.inst = Gpib.Gpib(0, 8)
        self.inst.write('MODE?')
        self.inst.read(100)

    def position(self):
        """Return current position."""
        self.inst.write("P:1")
        pos = int(self.inst.read(100))
        pos_mm = pos * 1E-4
        return pos_mm

    def move_to_origin(self):
        """Move to mechanical origin."""
        self.inst.write("H:1")

    def move_to_zero(self):
        """Move to electrical origin which can be varied."""
        self.inst.write("Z:1")

    def set_zero(self):
        """Set the current position as the electrical origin."""
        self.inst.write("R:1")

    def move_abs(self, pos, micron=False):
        """Move to the absolute position."""
        if micron:
            pos /= 1000
        if pos >= 0:
            command = 'M:w+P{}'.int(abs(pos * 1E4))
        else:
            command = 'M:w-P{}'.int(abs(pos * 1E4))
        self.inst.write(command)
        time.sleep(0.1)
        self.inst.write()

    def move_ref(self, move, micron=False):
        """Move relatively.

        Parameters
        -----------
        move: float
            travel distance. The default unit is mm.
        micron: Boolean
            if True, the unit of travel distance is micron (default: False)

        """
        if micron:
            move /= 1000
        if move >= 0:
            command = 'M:w+P{}'.int(abs(move * 1E4))
        else:
            command = 'M:w-P{}'.int(abs(move * 1E4))
        self.inst.write(command)
        time.sleep(0.1)
        self.inst.write()


if __name__ == '__main__':
    pass
