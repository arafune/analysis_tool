# -*- coding: utf-8 -*-
"""Module to analyze and show ARPES data."""

from __future__ import annotations


def wavelength2eV(wavelength_nm: float) -> float:
    """Return Energy of the light

    Parameters
    ----------
    wavelength_nm : float
        [description]

    Returns
    -------
    float
        [description]
    """
    planck_const: float = 6.62607015e-34  ##
    planck_const_eV: float = 4.135667696e-15
    light_velocity: int = 299792458

    #  (h*c = 1.2398419840550368e-6)
    return planck_const_eV * light_velocity / (wavelength_nm * 1e-9)
