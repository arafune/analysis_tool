"""Module to analyze and show ARPES data."""
from __future__ import annotations

from typing import TypeVar, reveal_type

import numpy as np
from numpy.typing import NDArray

A = TypeVar("A", NDArray[np.float_], float)


def delaytime_fs(mirror_movement_um: A) -> A:
    """Return delaytime from the mirror movement.

    Parameters
    ----------
    mirror_movement_um : float
        mirror movement in micron unit.

    Returns
    -------
    float
        delay time in fs.
    """
    return 3.335640951981521 * mirror_movement_um


def position2delaytime(position_mm: A, center_position_mm: float) -> A:
    """Return delay time from the mirror position.

    Parameters
    ----------
    position_mm: float
        mirror position
    center_position_mm: float
        mirror position corresponding to the zero delay

    Returns
    -------
        delay time in fs unit.
    """
    return delaytime_fs(2 * (position_mm - center_position_mm) * 1000)


def wavelength2eV(wavelength_nm: A) -> A:  # noqa: N802
    """Return Energy of the light.

    Parameters
    ----------
    wavelength_nm : float
        wavelength of the light in nm unit.

    Returns
    -------
    float
        Photon energy in eV unit.
    """
    planck_const_eV: float = 4.135667696e-15  # noqa: N806
    light_velocity: int = 299792458

    #  (h*c = 1.2398419840550368e-6)
    return planck_const_eV * light_velocity / (wavelength_nm * 1e-9)


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
    return e0 + (1 / (0.512410908328 * float(np.sqrt(mass))) ** 2) * k**2


reveal_type(float(np.sqrt(3.0)))


def parabolic_band_dispersion_angle(
    theta_degree: A,
    e0: float,
    mass: float = 1.0,
) -> A:
    """Return the energy at the given angle of emission (Free electron band).

    Energy reference is the vacuum level.
    (i.e. the energy is the kinetic energy, not final state energy)


    Parameters
    ----------
    theta_degree : float
        emission angle
    e0 : float
        energy at the Gamma point
    mass : float, optional
        electron mass, the static electron unit, by default 1.0

    Returns
    -------
    float
        Energy in eV unit measured from the vacuum level.
    """
    assert isinstance(theta_degree, np.ndarray | float)
    return e0 * mass / (mass - np.sin(np.deg2rad(theta_degree)) ** 2)


reveal_type(np.nan)
reveal_type(np.sin(np.deg2rad(np.array([1, 2, 3]))))
