#!/usr/bin/env python3
"""Delay line 用 module."""

import time
import Gpib


class FC104():
    """Class for Linear Translation feedback stage controller."""

    OVERLAP_POSITION = 0.0


    def __init__(self):
        """Initialization."""
        self.inst = Gpib.Gpib(0, 8)
        self.inst.write('MODE?')
        mode = self.inst.read(100)
        if b'LOCAL' in mode:
            self.inst.write('MODE:REMOTE')

    def _wait_for_ready(self):
        self.inst.write('SRQ:')
        srq = self.inst.read(100)
        wait_time = 0.1
        while b'B' in srq:
            time.sleep(wait_time)
            wait_time *= 2
            self.inst.write('SRQ:')
            srq = self.inst.read(100)

    def position(self):
        """Return current position."""
        self._wait_for_ready()
        self.inst.write("P:1")
        pos = int(self.inst.read(100))
        pos_mm = pos * 1E-4
        return pos_mm

    def move_to_origin(self):
        """Move to mechanical origin.
       
        And electric zero is set at this point.
        """
        self._wait_for_ready()
        self.inst.write("H:1")

    def move_to_zero(self):
        """Move to electrical origin which can be varied."""
        self._wait_for_ready()
        self.inst.write("Z:1")

    def set_zero(self):
        """Set the current position as the electrical origin."""
        self._wait_for_ready()
        self.inst.write("R:1")

    def move_abs(self, pos, micron=False):
        """Move to the absolute position."""
        self._wait_for_ready()
        if micron:
            eos /= 1000
        if pos >= 0:
            command = 'M:1+P{}'.format(int(abs(pos * 1E4)))
        else:
            command = 'M:1-P{}'.format(int(abs(pos * 1E4)))
        self.inst.write(command)
        time.sleep(0.1)
        self.inst.write('G')

    def move_ref(self, move, micron=False):
        """Move relatively.

        Parameters
        -----------
        move: float
            travel distance. The default unit is mm.
        micron: Boolean
            if True, the unit of travel distance is micron (default: False)

        """
        self._wait_for_ready()
        if micron:
            move /= 1000
        if move >= 0:
            command = 'M:1+P{}'.format(int(abs(move * 1E4)))
        else:
            command = 'M:1-P{}'.format(int(abs(move * 1E4)))
        self.inst.write(command)
        time.sleep(0.1)
        self.inst.write('G')

    def go_to_overlap():
        """Go to overlap opsition."""
        self._wait_for_ready()
        self.move_to_origin()
        self._wait_for_ready()
        self.move_abs(FC104.OVERLAP_POSITION)
        self._wait_for_ready()
        set_zero()


if __name__ == '__main__':
    pass
