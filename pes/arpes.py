# -*- coding: utf-8 -*-
"""Module to analyze and show ARPES data."""

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


class ARPESdata:
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
        self.second_axis = np.zeros(0)
        self.second_axis_name = ""

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

    def shift_2ndaxis(self, value):
        """Shift the second axis (Usually angle axis) by value."""
        self.second_axis += value

    def show(self, interpolation="nearest"):
        """Show the band data."""
        ax = plt.imshow(
            self.intensities.T,
            aspect="auto",
            interpolation=interpolation,
            origin="lower",
        )
        ax.axes.set_ylabel("Energy  ( eV )")
        if self.second_axis.size > 0:
            ax.set_extent(
                (
                    self.second_axis[0],
                    self.second_axis[-1],
                    self.energy_axis[0],
                    self.energy_axis[-1],
                )
            )
        else:
            ax.set_extent(
                (
                    0,
                    self.intensities.shape[0],
                    self.energy_axis[0],
                    self.energy_axis[-1],
                )
            )
        ax.axes.set_xlabel(self.second_axis_name)
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

    @property
    def angle_degs(self):
        """Alias of second_axis."""
        return self.second_axis

    def angle_shift(self, degree):
        """Shift the angle axis by "degree".

        Parameters
        -----------
        degree: float
            Value for shift angle

        """
        self.shift_2ndaxis(degree)

    def convert2band(self, angle_shift=0, energy_shift=0):
        """Return ARPESband object (The second axis is momentum).

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


class ARPESband(ARPESdata):
    """Class for ARPES data with wavenumber as the nonenergy axis.

    The main data (self.data) consists of three-column array.
    The first column is the momenta and the second is the energy
    and the third is the intensity. The length of the list is
    len('momentum') x len('angle'). The data is not simple Z-matrix
    shape as the ARPESmap data.

    Parameters
    -----------
    angles: list
        Emission angle axis.
    energies: list
        Kinetic Energy axis.  (Must be Kinetic energy: Measured from Ev.)
    intensities: list
        Photoemission intensity values

    Attributes
    -----------
    data: list
        Energy
    k_axis: list
        Momentum axis for *Grid style* (i.e. for intensities attribute).
    energy_axis: list
        Energy axis for *Grid style* (i.e. for intensities attribute).

    """

    def __init__(self, angles, energies, intensities):
        """Initialization."""
        super(ARPESband, self).__init__()
        degrees = np.pi / 180
        self.energy_axis = energies
        self.data = [np.zeros(0), np.zeros(0), np.zeros(0)]
        self.data[0] = np.tile(angles, (len(energies), 1)).T.flatten()
        self.data[1] = np.tile(energies, len(angles))
        self.data[0] = (
            0.512410908328
            * np.sqrt(self.data[1])
            * np.sin(self.data[0] * degrees)
        )
        self.data[2] = intensities.ravel()
        assert len(self.data[0]) == len(self.data[1]) == len(self.data[2])
        #
        n_energy = len(self.energy_axis)
        k_delta = np.abs(np.min(np.diff(self.data[0][0::n_energy])))
        k_max = np.max(self.data[0])
        k_min = np.min(self.data[0])
        self.second_axis = np.arange(k_min, k_max, k_delta)
        self.second_axis_name = "Parallel Momentum  (AA-1)"
        kaxis, eaxis = np.mgrid[
            k_min:k_max:k_delta,
            self.energy_axis[0] : self.energy_axis[-1] : n_energy * 1j,
        ]
        self.intensities = interpolate.griddata(
            points=np.array((self.data[0], self.data[1])).T,
            values=self.data[2],
            xi=(kaxis, eaxis),
        )

    @property
    def k_axis(self):
        """Alias for self.second_axis."""
        return self.second_axis


def make_arpesband(
    angles, energies, intensities, angle_shift=0, energy_shift=0
):
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
