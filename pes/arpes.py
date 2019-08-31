# -*- coding: utf-8 -*-
"""Module to analyze and show ARPES data."""

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


class ARPESdata():
    """Parent class for ARPESmap.

    Attributes
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
        """Show the band data."""
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
    """Class for ARPES intensity data.

    The "second axis" is the angle.

    Attributes
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

    def band_view(self, angle_shift=0, energy_shift=0):
        """Return ARPESband object.

        Parameters
        ------------
        angle_shift: float
            Value for angle shift
        energy_shift: float
            Value for energy shift

        Returns
        ----------
        ARPESBand

        """
        angles = self.angle_degs + angle_shift
        energies = self.energy_axis + energy_shift
        return ARPESband(angles, energies, self.intensities)

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
        ax.axes.set_ylabel("Angle ( deg )")
        return ax  # Not tested


class ARPESband():
    """Class for ARPES data with wavenumber as the nonenergy axis.

    The main data consists of three-column array. The first column is the
    momenta and the second is the energy and the third is the intensity.
    The length of the list is len('momentum') x len('angle').
    The data is not simple Z-matrix shape as the ARPESmap data.


    Attributes
    -----------

    data: list
        Energy
    k_axis: list
        momentum axis data for *Grid style*.
    energy_axis: list
        energy axis data for *Grid style*.


    """
    def __init__(self, angles, energies, intensities):
        """Initialization."""
        degrees = np.pi / 180
        self.k_axis = None
        self.energy_axis = energies
        self.data = [np.zeros(0), np.zeros(0), np.zeros(0)]
        self.data[0] = np.tile(angles, (len(energies), 1)).T.flatten()
        self.data[1] = np.tile(energies, len(angles))
        self.data[0] = 0.512410908328 * np.sqrt(self.data[1]) * np.sin(
            self.data[0] * degrees)
        self.data[2] = intensities.ravel()
        assert len(self.data[0]) == len(self.data[1]) == len(self.data[2])

    def griddata(self):
        """Return Griddata and detemine momentum axis.

        Returns
        ---------
        numpy.ndarray

        """

        n_energy = len(self.energy_axis)
        k_delta = np.abs(np.min(np.diff(self.data[0][0::n_energy])))
        k_max = np.max(self.data[0])
        k_min = np.min(self.data[0])
        self.k_axis = np.arange(k_min, k_max + k_delta, k_delta)
        kaxis, eaxis = np.mgrid[k_min:k_max + k_delta:k_delta, self.
                                energy_axis[0]:self.energy_axis[-1]:n_energy *
                                1j]
        #        return k_delta, k_max, k_min, self.k_axis

        return interpolate.griddata(points=np.array(self.data[0],
                                                    self.data[1]),
                                    values=self.data[2],
                                    xi=(kaxis, eaxis))

    def k_start_end(self):
        """Return the start and end momentum.

        Returns
        --------
            tuple: the value of the start and end axis

        """
        return min(self.data[0]), self(self.data[0])  # Not tested


def make_arpesband(angles,
                   energies,
                   intensities,
                   angle_shift=0,
                   energy_shift=0):
    """Make ARPES Band object.

    Parameters
    -----------
    angles: list
        angle data
    energies: list
        energy data
    intensity: list
        intensity data, len(intensity) = len(angles) * len(energies)
    angle_shift: float, default=0
        Value for Angle shift
    energy_shift: float, default=0
        Value for Energy shift

    Returns
    -------
    band: ARPESBand

    """
    angles += angle_shift
    energies += energy_shift
    return ARPESband(angles, energies, intensities)


#    def show(self, interpolation="nearest"):
#        """Show the band data.
#
#        Parameters
#        ----------
#        interpolation:str, default="nearest"
#            Interpolation method
#
#        """
#        ax = super(ARPESmap, self).show(interpolation)
#        ax.set_extent((
#            self.energy_axis[0],
#            self.energy_axis[-1],
#            self.k_axis[-1],
#        ))
#        ax.axes.set_ylabel("momentum  ( AA-1 )")
#        return ax  # Not teseted
#
