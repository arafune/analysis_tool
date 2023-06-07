# -*- coding: utf-8 -*-
"""Module to analyze and show ARPES data."""

from __future__ import annotations

import numpy as np


def delaytime_fs(mirror_movement_um: float) -> float:
    """Return delaytime from the mirror movement

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


def position2delaytime(position_mm: float, center_position_mm: float) -> float:
    """Return delay time from the mirror position

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


def wavelength2eV(wavelength_nm: float) -> float:
    """Return Energy of the light

    Parameters
    ----------
    wavelength_nm : float
        wavelength of the light in nm unit.

    Returns
    -------
    float
        Photon enery in eV unit.
    """
    planck_const: float = 6.62607015e-34  # J unit
    planck_const_eV: float = 4.135667696e-15
    light_velocity: int = 299792458

    #  (h*c = 1.2398419840550368e-6)
    return planck_const_eV * light_velocity / (wavelength_nm * 1e-9)


def parabolic_band_dispersion_k(k: float, e0: float, mass: float = 1.0) -> float:
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
    return e0 + (1 / (0.512410908328 * np.sqrt(mass)) ** 2) * k**2


def parabolic_band_dispersion_angle(
    theta_degree: float, e0: float, mass: float = 1.0
) -> float:
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
    return e0 * mass / (mass - np.sin(np.deg2rad(theta_degree)) ** 2)
