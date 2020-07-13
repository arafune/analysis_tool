#!/usr/bin/env python3
"""Collection of Selmeier equation."""

import numpy as np
from typing import Tuple


def air(lambda_micron: float) -> float:
    r"""Dispersion of air.

    https://refractiveindex.info/?shelf=other&book=air&page=Ciddor

    Parameters
    -----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.

    Returns
    ----------
    float:
        :math:`n`

    """
    return (
        1
        + 0.05792105 / (238.0185 - lambda_micron ** (-2))
        + 0.00167917 / (57.362 - lambda_micron ** (-2))
    )


def alphaBBO(lambda_micron: float) -> Tuple[float, float]:
    r"""Dispersion of :math:`\alpha`-BBO.

    http://www.newlightphotonics.com/Birefringent-Crystals/alpha-BBO-Crystals


    * Negative birefringence

    Parameters
    -----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.

    Return
    -------
    tuple:
        :math:`n_o` and :math:`n_e`

    """
    return (
        np.sqrt(
            2.67579
            + 0.02099 / (lambda_micron ** 2 - 0.00470)
            - 0.00528 * lambda_micron ** 2
        ),
        np.sqrt(
            2.31197
            + 0.01184 / (lambda_micron ** 2 - 0.01607)
            - 0.00400 * lambda_micron ** 2
        ),
    )


def betaBBO(lambda_micron: float) -> Tuple[float, float]:
    r"""Return :math:`n_o` and :math:`n_e` of :math:`\beta`-BBO.

    http://www.castech.com/manage/upfile/fileload/20170823144544.pdf

    * Negative birefringence

    Parameters
    -----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.

    Returns
    ---------
    tuple:
        :math:`n_o` and :math:`n_e`

    """
    return (
        np.sqrt(
            2.7359
            + 0.01878 / (lambda_micron ** 2 - 0.01822)
            - 0.01354 * lambda_micron ** 2
        ),
        np.sqrt(
            2.3753
            + 0.01224 / (lambda_micron ** 2 - 0.01667)
            - 0.01516 * lambda_micron ** 2
        ),
    )


def quartz(lambda_micron: float) -> Tuple[float, float]:
    r"""Dispersion of crystal quartz.

    Optics communications. 2011, vol. 284, issue 12, p. 2683-2686.

    Parameters
    -----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.

    Returns
    ---------
    tuple:
        :math:`n_o` and :math:`n_e`

    """
    return (
        np.sqrt(
            1.28604141
            + 1.07044083 * lambda_micron ** 2 / (lambda_micron ** 2 - 1.00585997 * 1e-2)
            + 1.10202242 * lambda_micron ** 2 / (lambda_micron ** 2 - 100)
        ),
        np.sqrt(
            1.28851804
            + 1.09509924 * lambda_micron ** 2 / (lambda_micron ** 2 - 1.02101864 * 1e-2)
            + 1.15662475 * lambda_micron ** 2 / (lambda_micron ** 2 - 100)
        ),
    )


def calcite(lambda_micron: float) -> Tuple[float, float]:
    r"""Dispersion of calcite.

    (:math:`\textrm{CaCO}_3`).

    http://www.redoptronics.com/Calcite-crystal.html

    * Negative birefringence

    Parameters
    -----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.

    Returns
    --------
    tuple:
        :math:`n_o` and :math:`n_e`

    """
    return (
        np.sqrt(
            1.28604141
            + 1.07044083 * lambda_micron ** 2 / (lambda_micron ** 2 - 1.00585997 * 1e-2)
            + 1.10202242 * lambda_micron ** 2 / (lambda_micron ** 2 - 100)
        ),
        np.sqrt(
            1.28851804
            + 1.09509924 * lambda_micron ** 2 / (lambda_micron ** 2 - 1.02101864 * 1e-2)
            + 1.15662475 * lambda_micron ** 2 / (lambda_micron ** 2 - 100)
        ),
    )
