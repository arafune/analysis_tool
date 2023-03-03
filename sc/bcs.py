import numpy as np
from numpy.typing import ArrayLike, NDArray


def gap_function(
    omega: NDArray[np.float_], delta: float, n_0: float, offset_x: float = 0
) -> NDArray[np.float_]:
    """Returns BCS gap function

    Parameters
    -----------
    omega: float
        Energy  (eV)
    delta: float
        Energy gap (eV)
    n_0: float
        Scaling factor
    offset_x: float
        offset value about energy axis
    """
    return n_0 * np.real(
        (
            np.abs((omega - offset_x))
            / np.emath.sqrt((omega - offset_x) ** 2 - delta**2)
        )
    )


def dynes(
    omega: NDArray[np.float_],
    delta: float,
    gamma: float,
    n_0: float,
    offset_x: float = 0,
) -> NDArray[np.float_]:
    """Return Dynes function

    Parameters
    -----------
    omega: float
        Energy  (eV)
    delta: float
        Energy gap (eV)
    gamma: float
        damping const (eV)
    n_0: float
        Scaling factor
    offset_x: float
        offset value about energy axis

    """
    return n_0 * np.real(
        np.abs(
            (omega - offset_x + (1.0j) * gamma)
            / (np.emath.sqrt((omega - offset_x + (1.0j) * gamma) ** 2 - delta**2))
        )
    )


def diff_fd(omega: NDArray[np.float_], temp: float) -> NDArray[np.float_]:
    """Return differential of the Fermi-Dirac distribution

    Paramters
    ----------
    omega: float
        Energy  (eV).
    temp: float
        Temperature (Kelvin)
    """
    k = 8.617333262e-5  # (eV)
    return -np.exp(omega / (k * temp)) / (
        (1 + np.exp(omega / (k * temp))) ** 2 * k * temp
    )


def extend_energy_axis(energy_axis: NDArray[np.float_]) -> NDArray[np.float_]:
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
    min_energy: ArrayLike = np.min(energy_axis)
    max_energy: ArrayLike = np.max(energy_axis)
    return np.linspace(
        (min_energy + max_energy) / 2 - (max_energy - min_energy),
        (min_energy + max_energy) / 2 + (max_energy - min_energy),
        len(energy_axis) * 5,
    )


def conv_gap(
    omega: float,
    energy_axis: NDArray[np.float_],
    delta: float,
    n_0: float,
    temperature: float,
    offset_x: float = 0,
) -> NDArray[np.float_]:
    """Returns the BCS gap function convoluted by differentiated Fermi-Dirac.

    Parameters
    -----------
    omega:
        Energy
    energy_axis: NDArray[np.float]
        Energy axis (Used in interpolation process internally)
    omega: float
        Energy (eV)
    delta: float
        Energy (eV)
    n_0: float
        Scale parameter
    temperature: float
        temperature (Kelvin)
    offset_x: float
        offset value about energy axis (default=0)

    Returns
    -------
    float:
        The tunneling current
    """
    the_gap = gap_function(energy_axis, delta, n_0, offset_x)
    # the_gap = gap_function(extend_energy_axis(omega), delta, n_0, offset_x)
    the_dfd = diff_fd(energy_axis, temperature)
    # the_dfd = diff_fd(extend_energy_axis(omegaa), temperature)
    return np.interp(
        omega,
        energy_axis,
        np.convolve(the_gap, -the_dfd, "same")
        * np.abs(energy_axis[0] - energy_axis[1]),
    )


def conv_dynes(
    omega: float,
    energy_axis: NDArray[np.float_],
    delta: float,
    gamma: float,
    n_0: float,
    temperature: float,
    offset_x: float = 0,
) -> NDArray[np.float_]:
    """Returns the Dynes function convoluted by differentiated Fermi-Dirac.

    Parameters
    -----------
    omega:
        Energy
    energy_axis: NDArray[np.float]
        Energy axis (Used in interpolation process internally)
    omega: float
        Energy (eV)
    delta: float
        Energy (eV)
    gamma: float
        Damping constant (eV)
    n_0: float
        Scale parameter
    temperature: float
        temperature (Kelvin)
    offset_x: float
        offset value about energy axis (default=0)

    Returns
    -------
    float:
        The tunneling current
    """
    the_gap = dynes(energy_axis, delta, gamma, n_0, offset_x)
    # the_gap = dynes(extend_energy_axis(omega), delta, gamma, n_0, offset_x)
    the_dfd = diff_fd(energy_axis, temperature)
    # the_dfd = diff_fd(extend_energy_axis(omegaa), temperature)
    return np.interp(
        omega,
        energy_axis,
        np.convolve(the_gap, -the_dfd, "same")
        * np.abs(energy_axis[0] - energy_axis[1]),
    )
