#!/usr/bin/env python3
"""Collection of Sellmeier equation."""

from __future__ import annotations

import numpy as np


def three_term_sellmier(lambda_micron, a, b, c, d, e, f) -> float:
    r"""
    :math:`n^2 -1 = \frac{a \lambda^2}{\lambda^2 - b} + \frac{c \lambda^2}{\lambda^2 - d} + \frac{e \lambda^2}{\lambda^2 - f}`


    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    a: float
        Coefficient a
    b: float
        Coefficient b
    c: float
        Coefficient c
    d: float
        Coefficient d
    e: float
        Coefficient e
    f: float
        Coefficient f

    Returns
    -------
    float
        Calculated refractive index
    """
    n2 = (
        1
        + a * lambda_micron**2 / (lambda_micron**2 - b)
        + c * lambda_micron**2 / (lambda_micron**2 - d)
        + e * lambda_micron**2 / (lambda_micron**2 - f)
    )
    return np.sqrt(n2)


def second_derivative_three_term_sellmier(lambda_micron, a, b, c, d, e, f) -> float:
    """Second derivative of the three term sellmier equation

    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    a: float
        Coefficient a
    b: float
        Coefficient b
    c: float
        Coefficient c
    d: float
        Coefficient d
    e: float
        Coefficient e
    f: float
        Coefficient f

    Returns
    -------
    float
        Calculated refractive index
    """
    return (
        -4
        * lambda_micron**2
        * (
            (a * b) / (b - lambda_micron**2) ** 2
            + (c * d) / (d - lambda_micron**2) ** 2
            + (e * f) / (f - lambda_micron**2) ** 2
        )
        ** 2
        + 2
        * (
            1
            + (a * lambda_micron**2) / (-b + lambda_micron**2)
            + (c * lambda_micron**2) / (-d + lambda_micron**2)
            + (e * lambda_micron**2) / (-f + lambda_micron**2)
        )
        * (
            (-2 * a * b * (b + 3 * lambda_micron**2)) / (b - lambda_micron**2) ** 3
            - (2 * c * d * (d + 3 * lambda_micron**2)) / (d - lambda_micron**2) ** 3
            - (2 * e * f * (f + 3 * lambda_micron**2)) / (f - lambda_micron**2) ** 3
        )
    ) / (
        4.0
        * (
            1
            + (a * lambda_micron**2) / (-b + lambda_micron**2)
            + (c * lambda_micron**2) / (-d + lambda_micron**2)
            + (e * lambda_micron**2) / (-f + lambda_micron**2)
        )
        ** 1.5
    )


def two_term_serllmier(lambda_micron, a, b, c, d) -> float:
    r"""
    :math:`n^2 -1 = \frac{a \lambda^2}{\lambda^2 - b} + \frac{c \lambda^2}{\lambda^2 - d}`


    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    a: float
        Coefficient a
    b: float
        Coefficient b
    c: float
        Coefficient c
    d: float
        Coefficient d

    Returns
    -------
    float
        Calculated refractive index
    """
    return three_term_sellmier(lambda_micron, a, b, c, d, 0, 0)


def second_derivative_two_term_seellmier(lambda_micron, a, b, c, d) -> float:
    """Second derivative of the two term sellmier equation

    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    a: float
        Coefficient a
    b: float
        Coefficient b
    c: float
        Coefficient c
    d: float
        Coefficient d

    Returns
    -------
    float
        Calculated refractive index
    """
    return second_derivative_three_term_sellmier(lambda_micron, a, b, c, d, 0, 0)


def BK7(lambda_micron: float, second_derivative: bool = False) -> float:
    r"""Dispersion of BK7

    https://refractiveindex.info/?shelf=glass&book=BK7&page=SCHOTT

    Parameters
    -----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.
    second_derivative: bool
        if True return :math:`\frac{d^2n}{d\lambda^2}`
    """
    a = 1.03961212
    b = 0.00600069867
    c = 0.231792344
    d = 0.0200179144
    e = 1.01046945
    f = 103.560653
    if second_derivative:
        return second_derivative_three_term_sellmier(lambda_micron, a, b, c, d, e, f)
    return three_term_sellmier(lambda_micron, a, b, c, d, e, f)


def FusedSilica(lambda_micron: float, second_derivative: bool = False) -> float:
    r"""Dispersion of Fusd Silica

    https://refractiveindex.info/?shelf=glass&book=fused_silica&page=Malitson

    Parameters
    -----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.
    second_derivative: bool
        if True return :math:`\frac{d^2n}{d\lambda^2}`
    """
    a = 0.6961663
    b = 0.06840432
    c = 0.4079426
    d = 0.11624142
    e = 0.8974794
    f = 9.8961612
    if second_derivative:
        return second_derivative_three_term_sellmier(lambda_micron, a, b, c, d, e, f)
    return three_term_sellmier(lambda_micron, a, b, c, d, e, f)


def air(lambda_micron: float, second_derivative: bool = False) -> float:
    r"""Dispersion of air.

    https://refractiveindelambda_micron.info/?shelf=other&book=air&page=Ciddor

    Parameters
    -----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.
    second_derivative: bool
        if True return :math:`\frac{d^2n}{d\lambda^2}`

    Returns
    ----------
    float:
        :math:`n`
    """
    a = 0.05792105
    b = 238.0185
    c = 0.00167917
    d = 57.362
    if second_derivative:
        return (2 * a * (1 + 3 * b * lambda_micron**2)) / (
            -1 + b * lambda_micron**2
        ) ** 3 + (2 * (c + 3 * c * d * lambda_micron**2)) / (
            -1 + d * lambda_micron**2
        ) ** 3
    return 1 + a / (b - lambda_micron ** (-2)) + c / (d - lambda_micron ** (-2))


def alphaBBO(lambda_micron: float) -> tuple[float, float]:
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
            + 0.02099 / (lambda_micron**2 - 0.00470)
            - 0.00528 * lambda_micron**2
        ),
        np.sqrt(
            2.31197
            + 0.01184 / (lambda_micron**2 - 0.01607)
            - 0.00400 * lambda_micron**2
        ),
    )


def betaBBO(lambda_micron: float) -> tuple[float, float]:
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
            + 0.01878 / (lambda_micron**2 - 0.01822)
            - 0.01354 * lambda_micron**2
        ),
        np.sqrt(
            2.3753
            + 0.01224 / (lambda_micron**2 - 0.01667)
            - 0.01516 * lambda_micron**2
        ),
    )


def quartz(lambda_micron: float) -> tuple[float, float]:
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
            + 1.07044083 * lambda_micron**2 / (lambda_micron**2 - 1.00585997 * 1e-2)
            + 1.10202242 * lambda_micron**2 / (lambda_micron**2 - 100)
        ),
        np.sqrt(
            1.28851804
            + 1.09509924 * lambda_micron**2 / (lambda_micron**2 - 1.02101864 * 1e-2)
            + 1.15662475 * lambda_micron**2 / (lambda_micron**2 - 100)
        ),
    )


def calcite(lambda_micron: float) -> tuple[float, float]:
    r"""Dispersion of calcite.  (:math:`\mathrm{CaCO}_3`).

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
            + 1.07044083 * lambda_micron**2 / (lambda_micron**2 - 1.00585997 * 1e-2)
            + 1.10202242 * lambda_micron**2 / (lambda_micron**2 - 100)
        ),
        np.sqrt(
            1.28851804
            + 1.09509924 * lambda_micron**2 / (lambda_micron**2 - 1.02101864 * 1e-2)
            + 1.15662475 * lambda_micron**2 / (lambda_micron**2 - 100)
        ),
    )


def mgf2(lambda_micron: float) -> tuple[float, float]:
    no = np.sqrt(
        1
        + 0.4876 * lambda_micron**2 / (lambda_micron**2 - 0.0434**2)
        + 0.3988 * lambda_micron**2 / (lambda_micron**2 - 0.0946**2)
        + 2.3120 * lambda_micron**2 / (lambda_micron**2 - 23.7936**2)
    )
    ne = np.sqrt(
        1
        + 0.4134 * lambda_micron**2 / (lambda_micron**2 - 0.0368**2)
        + 0.5050 * lambda_micron**2 / (lambda_micron**2 - 0.0908**2)
        + 2.4905 * lambda_micron**2 / (lambda_micron**2 - 23.7720**2)
    )
    return (no, ne)


def phase_matching_angle_bbo(fundamental_micron: float) -> float:
    """Phase matching angle of beta-BBO for SHG

    Parameters
    ----------
    fundamental_micron : float
        wavelength of fundamental light

    Returns
    -------
    float
        Phase matching angle (Unit: Degree)
    """
    sin2theta = (
        (betaBBO(fundamental_micron)[0]) ** (-2)
        - (betaBBO(fundamental_micron / 2)[0] ** (-2))
    ) / (
        (betaBBO(fundamental_micron / 2)[1]) ** (-2)
        - (betaBBO(fundamental_micron / 2)[0] ** (-2))
    )
    return np.rad2deg(np.arcsin(np.sqrt(sin2theta)))
