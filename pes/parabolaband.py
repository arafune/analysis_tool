#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Energy band with parabolic dispersion

簡単な話なんだけど、何度も迷ってしまっているので、一度ライブラリーにしておこう。
"""

import numpy as np


def dispersion_k(k: float, e0: float, mass: float = 1.0) -> float:
    """Return the energy at the given k-point.

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
    return e0 + (1 / (0.512 * np.sqrt(mass)) ** 2) * k ** 2


def dispersion_angle(theta_degree: float, e0: float, mass: float = 1.0) -> float:
    """Return the energy at the given angle of emission.

    Energy reference is the vacuum level.
    (i.e. the energy is the kinetic energy, not final state energy)

    E_k ~= E0 + (E0/m) theta**2

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
