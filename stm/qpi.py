# -*- coding: utf-8 -*-
'''.. py:module:: qpi

Module to extract the line profile data about QPI results.
'''

import numpy as np
import os.path


class QPI(object):
    '''.. py:class:: QPI(array-like)

    Class for QPI data

    Attributes
    ------------
    data: tuple, list, np.ndarray
       1D or 2D matrix data.  The size of data should be n**2. 
    physical_size: float
       The length of the horizontal line.
    bias: float
       The bias voltage in V unit.
    current
       The tunneling current in nA unit.
    '''

    def __init__(self, data, physical_size=0, bias=0, current=0, dataname=''):
        self.data = np.array(data, dtype=np.float_)
        if self.data.ndim == 1:
            self.pixels = int(np.sqrt(self.data.shape[0]))
            self.data = self.data.reshape(self.pixels, self.pixels)
        elif self.data.ndim == 2 and self.data.shape[0] == self.data.shape[1]:
            self.pixels = self.data.shape[0]
        else:
            raise ValueError("Data mismatch!")
        if physical_size == 0:
            self.physical_size = self.data.shape[0]
        else:
            self.physical_size = physical_size
        self.bias = bias
        self.current = current
        self.dataname = dataname

    def cross_section_by_degree(self, angle):
        '''Calculated the intensity along the line tilted by the angle'''
        degree = np.pi / 180.0
        if -1.0 < np.tan(angle * degree) <= 1.0:
            position_pixel = [(x, self.ypixel(x, angle))
                              for x in range(self.pixels)]
        else:
            position_pixel = [(int((y - self.pixels / 2.0) /
                                   np.tan(angle * degree) +
                                   self.pixels / 2.0), y)
                              for y in range(self.pixels)]
        return np.array([self.data[pos] for pos in position_pixel])

    def ypixel(self, x, angle):
        '''Calculate y pixel with quantization-error correction'''
        degree = np.pi / 180.0
        y = int(np.tan(angle * degree) *
                (x - self.pixels / 2.0) + self.pixels / 2.0)
        if y >= self.pixels:
            y = self.pixels-1
        elif y < 0:
            y = 0
        return y

    def physical_axis(self, angle):
        '''Calculate k-value along the line tilted by the angle'''
        degree = np.pi / 180.0
        if -1.0 <= np.tan(angle * degree) <= 1.0:
            return np.linspace(- self.physical_size / 2.0 *
                               np.abs(1 / np.cos(angle * degree)),
                               self.physical_size / 2.0 *
                               np.abs(1 / np.cos(angle * degree)),
                               self.pixels)
        else:
            return np.linspace(- self.physical_size / 2.0 *
                               np.abs(1 / np.sin(angle * degree)),
                               self.physical_size / 2.0 *
                               np.abs(1 / np.sin(angle * degree)),
                               self.pixels)


def qpidataload(filename):
    '''.. py:function:: qpidataload(file)

    Data loader for the file converted from SM4

    Parameters
    ----------
    filename: str
       The file name of SM4-file.

    Returns
    -------
        QPI: QPI object
    '''
    dataname = os.path.splitext(filename)[0]
    thefile = open(filename)
    data = []
    with thefile:
        [next(thefile) for i in range(4)]
        tmp = next(thefile)
        bias, bias_unit, current = (float(tmp.split()[3]),
                                        tmp.split()[4], float(tmp.split()[6]))
        if bias_unit in "mV,":
            bias = float(bias) / 1000
        [next(thefile) for i in range(2)]
        xdim = float(next(thefile).split()[2])
        [next(thefile) for i in range(5)]
        for line in thefile:
            data.append(line.split()[1:])
    return QPI(data, physical_size=xdim, bias=bias,
               current=current, dataname=dataname)


def anglestring(angle):
    '''.. py:function::anglestring(angle)

    parameters
    -----------
    angle: float
          The angle.


    Returns
    ---------
    str
          When the angle is negative, return 'm'+abs(angle).

'''
    if angle < 0:
        return "m"+str(abs(angle))
    else:
        return str(angle)
