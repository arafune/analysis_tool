#! /usr/bin/env python3
"""HREELS basic parameters"""

import numpy as np

DEGREE: float = np.pi / 180.0


def scatter_angle(theta_in_deg: float) -> float:
    """Return the minimum scattering angle.

    The angle of of rotation about the detector is 78 degree measured from straight geometry.

    Parameters
    ----------
    theta_in_deg: float
        Incident angle

    Returns
    -------
    float
        Minimum scattering angle achieved by IB500
    """
    return 102.0 - theta_in_deg


def momentum_transfer(
    energy_eV: float, theta_in_deg: float, theta_out_deg: float
) -> float:
    """Return the momentum transfer in off-specular geometry of EELS experiments.

        Parameters
        ----------
        energy_eV: float
            Energy of impact electron (eV unit)
        theta_in_deg: float
            Incident angle
        theta_out_deg: float
            Scattering angle
    s
        Returns
        -------
        float
            Transfered momentum (AA-1 units)
    """
    return (
        0.512
        * np.sqrt(energy_eV)
        * (np.sin(theta_in_deg * DEGREE) - np.sin(theta_out_deg * DEGREE))
    )
