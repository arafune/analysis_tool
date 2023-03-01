import numpy as np
from numpy.typing import ArrayLike, NDArray


def gap_function(omega: ArrayLike, delta: float, n_0: float) -> float:
    """Returns BCS gap function


    Parameters
    -----------
    omega: float
        Energy  (eV)
    delta: float
        Energy gap (eV)
    n_0: float
        :Scaling factor
    """
    return n_0 * np.real((np.abs(omega) / np.emath.sqrt(omega**2 - delta**2)))


def diff_fd(omega: ArrayLike, temp: float) -> float:
    """Return differential of the Fermi-Dirac distribution

    Paramters
    ----------
    omega: float
        Energy  (eV).
    temp: float
        Temperature (Kelvin)
    """
    k = 8.617333262e-5  # (mev)
    return -np.exp(omega / (k * temp)) / (
        (1 + np.exp(omega / (k * temp))) ** 2 * k * temp
    )


def extend_energy_axis(energy_axis: ArrayLike) -> NDArray:
    """Return the array extended.

    Parameters
    ----------
    energy_axis : ArrayLike
        _description_

    Returns
    -------
    NDArray
        _description_
    """
    # expand the energy region
    min_energy: float = np.min(energy_axis)
    max_energy: float = np.max(energy_axis)
    return np.linspace(
        (min_energy + max_energy) / 2 - (max_energy - min_energy),
        (min_energy + max_energy) / 2 + (max_energy - min_energy),
        len(energy_axis) * 5,
    )


def conv_gap(
    omega: float, energy_axis: ArrayLike, delta: float, n_0: float, temperature: float
) -> float:
    """Returns the convoluted BCS gap function.

    Parameters
    -----------
    omega:
        Energy
    energy_axis: NDArray[np.float]
        Energy axis (Used in interpolation process)
    omega: float
        Energy (eV)
    delta: float
        Energy (eV)
    n_0: float
        Scale parameter
    temperature: float
        temperature (Kelvin)

    Returns
    -------
    float:
        The tunneling current
    """
    the_gap = gap_function(energy_axis, delta, n_0)
    the_dfd = diff_fd(energy_axis, temperature)
    # return np.convolve(the_gap, -the_dfd, "same") / np.abs(energy_axis[0]-energy_axis[1])
    return np.interp(
        omega,
        energy_axis,
        np.convolve(the_gap, -the_dfd, "same")
        * np.abs(energy_axis[0] - energy_axis[1]),
    )
