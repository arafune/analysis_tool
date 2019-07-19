# -*- coding: utf-8 -*-
"""Module to analyze and show ARPES data.

.. py:module:: areps
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


class ARPESdata(object):
    """Parent class for ARPESmap and ARPESband.

    .. py:class:: ARPESdata
    """

    def __init__(self):
        self.intensities = np.zeros(0)
        self.energy_axis = np.zeros(0)

    def energy_start_end(self):
        """Return start and end energies.

        .. py:method:: energy_start_end()

        Returns
        --------
            tuple: the value of the start and end energies

        """
        return self.energy_axis[0], self.energy_axis[-1]  # Not tested

    def energy_shift(self, energy):
        """Shift the energy axis by "energy".

        .. py:method:: energy_shift(energy)

        """
        self.energy_axis = self.energy_axis + energy

    def show(self, interpolation="nearest"):
        """Show the band data.

        .. py:method:: show()
        """
        ax = plt.imshow(self.intensities,
                        aspect="auto",
                        interpolation=interpolation)
        ax.axes.set_xlabel("Energy  ( eV )")
        ax.set_extent((self.energy_axis[0], self.energy_axis[-1],
                       self.intensities.shape[0], 0))
        return ax  # Not tested

    def showspectra(self, spacing="auto", color="blue"):
        """Show the waterfall view.

        .. py:method:: show()

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
        if spacing == "auto":
            spacing = int(maxintensity * 7 / 2 / numspectra)
        for no, spectrum in enumerate(reversed(self.intensities)):
            ax.plot(self.energy_axis, spectrum + spacing * no, color=color)
        return fig, ax  # Not tested


class ARPESmap(ARPESdata):
    """Class for ARPES intensity data  with infomation of physical axes.

    .. py:class:: ARPESmap()
    """

    def __init__(self):
        super(ARPESmap, self).__init__()
        self.angle_axis = np.zeros(0)

    def angle_start_end(self):
        """Return the start and end energies.

        .. py:method:: angle_start_end()

        Returns
        --------
            tuple: the value of the start and end axis

        """
        return self.angle_axis[0], self.angle_axis[-1]  # Not tested

    def angle_shift(self, degree):
        """Shift the angle  axis by "degree".

        .. py:method:: angle_shift(degree)
        """
        self.angle_axis = self.angle_axis + degree

    def show(self, interpolation="nearest"):
        """Show the band data.

        .. py:method:: show()
        """
        ax = super(ARPESmap, self).show(interpolation)
        ax.set_extent((
            self.energy_axis[0],
            self.energy_axis[-1],
            self.angle_axis[-1],
            self.angle_axis[0],
        ))
        ax.axes.set_ylabel("Angle  ( deg )")
        return ax  # Not tested


class ARPESband(ARPESdata):
    """Class for ARPES data with wavenumber as the  nonenergy axis.

    .. py:class:: ARPESband()
    """

    def __init__(self):
        super(ARPESmap, self).__init__()
        self.k_axis = np.zeros(0)  # Not tested

    def k_start_end(self):
        """Return the start and end momentum.

        .. py:method:: k_start_end()

        Returns
        --------
            tuple: the value of the start and end axis

        """
        return self.k_axis[0], self.k_axis[-1]  # Not tested

    def k_shift(self, momentum):
        """Shift the k-axis by "momentum".

        .. py:method:: k_shift(energy)
        """
        self.k_axis = self.k_axis + momentum  # Not teseted

    def show(self, interpolation="nearest"):
        """Show the band data.

        .. py:method:: show()

        """
        ax = super(ARPESmap, self).show(interpolation)
        ax.set_extent((self.energy_axis[0], self.energy_axis[-1],
                       self.k_axis[-1], self.k_axis[0]))
        ax.axes.set_ylabel("momentum  ( AA-1 )")
        return ax  # Not teseted
