# -*- coding: utf-8 -*-
""".. py:module:: areps

Module to analyze and show ARPES data
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


class ARPESdata(object):
    """.. py:class:: ARPESdata
    Parent class for ARPESmap and ARPESband
    """

    def __init__(self):
        self.intensities = np.zeros(0)
        self.energy_axis = np.zeros(0)

    def energy_start_end(self):
        """.. py:method:: energy_start_end()

        Returns
        --------
            tuple: the value of the start and end energies
        """
        return self.energy_axis[0], self.energy_axis[-1],

    def energy_shift(self, energy):
        """.. py:method:: energy_shift(energy)

        Shift the energy axis by "energy"
        """
        self.energy_axis = self.energy_axis + energy

    def show(self, interpolation='nearest'):
        """.. py:method:: show()

        Show the band data
        """
        ax = plt.imshow(
            self.intensities, aspect='auto', interpolation=interpolation)
        ax.axes.set_xlabel('Energy  ( eV )')
        ax.set_extent((self.energy_axis[0], self.energy_axis[-1],
                       self.intensities.shape[0], 0))
        return ax

    def showspectra(self, spacing='auto', color='blue'):
        """.. py:method:: show()

        Show the waterfall view

        Parameters
        -----------
        spacing: text, float
            The y(non-energy axis)-offset between the neighboring spectra.
        """
        numspectra = self.intensities.shape[0]
        maxintensity = np.max(self.intensities)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        maxintensity = np.max(self.intensities)
        if spacing == 'auto':
            spacing = int(maxintensity * 7 / 2 / numspectra)
        for no, spectrum in enumerate(reversed(self.intensities)):
            ax.plot(self.energy_axis, spectrum + spacing * no, color=color)
        return fig, ax


class ARPESmap(ARPESdata):
    """.. py:class:: ARPESmap()

    Class for ARPES intensity data  with infomation of physical axes.
"""

    def __init__(self):
        super(ARPESmap, self).__init__()
        self.angle_axis = np.zeros(0)

    def angle_start_end(self):
        """.. py:method:: angle_start_end()

        Returns
        --------
            tuple: the value of the start and end axis
        """
        return self.angle_axis[0], self.angle_axis[-1]

    def angle_shift(self, angle):
        """.. py:method:: angle_shift(energy)

        Shift the angle  axis by "angle"
        """
        self.angle_axis = self.angle_axis + angle

    def show(self, interpolation='nearest'):
        """.. py:method:: show()

        Show the band data
        """
        ax = super(ARPESmap, self).show(interpolation)
        ax.set_extent((self.energy_axis[0], self.energy_axis[-1],
                       self.angle_axis[-1], self.angle_axis[0]))
        ax.axes.set_ylabel('Angle  ( deg )')
        return ax


class ARPESband(ARPESdata):
    """.. py:class:: ARPESband()

    Class for ARPES data with wavenumber as the  nonenergy axis.
    """

    def __init__(self):
        super(ARPESmap, self).__init__()
        self.k_axis = np.zeros(0)

    def k_start_end(self):
        """.. py:method:: k_start_end()

        Returns
        --------
            tuple: the value of the start and end axis
        """
        return self.k_axis[0], self.k_axis[-1]

    def k_shift(self, k):
        """.. py:method:: k_shift(energy)

        Shift the k-axis by "k"
        """
        self.k_axis = self.k_axis + k

    def show(self, interpolation='nearest'):
        """.. py:method:: show()

        Show the band data
        """
        ax = super(ARPESmap, self).show(interpolation)
        ax.set_extent((self.energy_axis[0], self.energy_axis[-1],
                       self.k_axis[-1], self.k_axis[0]))
        ax.axes.set_ylabel('momentum  ( AA-1 )')
        return ax
