# -*- coding: utf-8 -*-
"""Module to analyze and show ARPES data."""

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


class ARPESdata(object):
    """Parent class for ARPESmap and ARPESband.

    Parameters
    -----------
    intensities: numpy.array
        Photoemission intensity
    energy_axis: numpy.array
        Energy

    """
    def __init__(self):
        """Initialization."""
        self.intensities = np.zeros(0)
        self.energy_axis = np.zeros(0)

    def energy_start_end(self):
        """Return start and end energies.

        Returns
        --------
        tuple: the value of the start and end energies

        """
        return self.energy_axis[0], self.energy_axis[-1]  # Not tested

    def energy_shift(self, energy):
        """Shift the energy axis by "energy".

        Parameters
        ----------
        energy: float
            Energy shift

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
        ax.set_extent((
            self.energy_axis[0],
            self.energy_axis[-1],
            self.intensities.shape[0],
            0,
        ))
        return ax  # Not tested

    def showspectra(self, spacing="auto", color="blue"):
        """Show the waterfall view.

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
    """Class for ARPES intensity data with infomation of physical axes.

    Parameters
    -----------
    angles_degs: numpy.array
        Emission angle

    """
    def __init__(self):
        """Initialization."""
        super(ARPESmap, self).__init__()
        self.angle_degs = np.zeros(0)

    def angle_start_end(self):
        """Return the start and end energies.

        Returns
        --------
            tuple: the value of the start and end axis

        """
        return self.angle_degs[0], self.angle_degs[-1]  # Not tested

    def angle_shift(self, degree):
        """Shift the angle  axis by "degree"."""
        self.angle_degs = self.angle_degs + degree

    def show(self, interpolation="nearest"):
        """Show the band data.

        Parameters
        ------------
        interpolation: str, default="nearest"
            Interpolation method

        """
        ax = super(ARPESmap, self).show(interpolation)
        ax.set_extent((
            self.energy_axis[0],
            self.energy_axis[-1],
            self.angle_degs[-1],
            self.angle_degs[0],
        ))
        ax.axes.set_ylabel("Angle  ( deg )")
        return ax  # Not tested


class ARPESband(ARPESdata):
    """Class for ARPES data with wavenumber as the  nonenergy axis.

    Attributes
    -----------
    k_axis: numpy.array
        momentum axis

    """
    def __init__(self):
        """Initialization."""
        super(ARPESmap, self).__init__()
        self.k_axis = np.zeros(0)  # Not tested

    def k_start_end(self):
        """Return the start and end momentum.

        Returns
        --------
            tuple: the value of the start and end axis

        """
        return self.k_axis[0], self.k_axis[-1]  # Not tested

    def k_shift(self, momentum):
        """Shift the k-axis by "momentum".

        Parameters
        -----------
        momentum: float
            Momentum shift

        """
        self.k_axis = self.k_axis + momentum  # Not teseted

    def show(self, interpolation="nearest"):
        """Show the band data.

        Parameters
        ----------
        interpolation:str, default="nearest"
            Interpolation method

        """
        ax = super(ARPESmap, self).show(interpolation)
        ax.set_extent((
            self.energy_axis[0],
            self.energy_axis[-1],
            self.k_axis[-1],
            self.k_axis[0],
        ))
        ax.axes.set_ylabel("momentum  ( AA-1 )")
        return ax  # Not teseted
