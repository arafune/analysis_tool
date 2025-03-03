"""Module to analyze and show ARPES data."""

from __future__ import annotations

from typing import TypeVar

import numpy as np
from numpy.typing import NDArray

A = TypeVar("A", NDArray[np.float64], float)


def parabolic_band_dispersion_k(k: A, e0: float, mass: float = 1.0) -> A:
    """Return the energy at the given k-point .

    Energy reference is the vacuum level.
    (i.e. the energy is the kinetic energy, not final state energy)

    Parameters
    ----------
    k : float
        parallel momentum A-1 unit
    e0 : float
        energy at the Gamma point
    mass : float, optional
        electron mass, the static electron unit, by default 1.0

    Returns
    -------
    float
        Energy in eV unit measured from the vacuum level.

    """
    assert isinstance(k, np.ndarray | float)
    assert isinstance(np.sqrt, float)
    return e0 + (1 / (0.512410908328 * mass**0.5) ** 2) * k**2


def parabolic_band_dispersion_angle(
    theta_rad: A,
    e0: float,
    mass: float = 1.0,
    wf_offset: float = 0.0,
) -> A:
    """Return the energy at the given angle of emission (Free electron band).

    Energy reference is the vacuum level.
    (i.e. the energy is the kinetic energy, not final state energy)


    Parameters
    ----------
    theta_rad : float
        emission angle
    e0 : float
        energy at the Gamma point
    mass : float, optional
        electron mass, the static electron unit, by default 1.0
    wf_offset : float, optional
        Offset corresponding to the (analyzer) work function, by default 0.0

    Returns
    -------
    float
        Energy in eV unit measured from the vacuum level.

    """
    return (e0 - wf_offset) * mass / (mass - np.sin(theta_rad) ** 2)
