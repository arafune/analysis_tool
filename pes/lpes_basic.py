# -*- coding: utf-8 -*-
"""Module to analyze and show ARPES data."""

from __future__ import annotations


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
