#!/usr/bin/env python3
"""Collection of Sellmeier equation."""

from __future__ import annotations

import numpy as np


def three_term_sellmier(
    lambda_micron: float,
    b1: float,
    c1: float,
    b2: float,
    c2: float,
    b3: float,
    c3: float,
) -> float:
    r"""
    :math:`n^2 -1 = \frac{B_1 \lambda^2}{\lambda^2 - c1} +
    \frac{B_1 \lambda^2}{\lambda^2 - C_2} + \frac{B_3 \lambda^2}{\lambda^2 - C_3}`


    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    b1: float
        Coefficient B_1
    c1: float
        Coefficient C_1
    b2: float
        Coefficient B_2
    c2: float
        Coefficient C_2
    b3: float
        Coefficient B_3
    c3: float
        Coefficient C_3

    Returns
    -------
    float
        Calculated refractive index
    """
    n2 = (
        1
        + b1 * lambda_micron**2 / (lambda_micron**2 - c1**2)
        + b2 * lambda_micron**2 / (lambda_micron**2 - c2**2)
        + b3 * lambda_micron**2 / (lambda_micron**2 - c3**2)
    )
    return np.sqrt(n2)


def second_derivative_three_term_sellmier(
    lambda_micron: float,
    b1: float,
    c1: float,
    b2: float,
    c2: float,
    b3: float,
    c3: float,
) -> float:
    """Second derivative of the three term sellmier equation

    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    b1: float
        Coefficient B_1
    c1: float
        Coefficient C_1
    b2: float
        Coefficient B_2
    c2: float
        Coefficient C_2
    b3: float
        Coefficient B_2
    c3: float
        Coefficient C_3

    Returns
    -------
    float
        Calculated refractive index
    """
    return (
        -4
        * lambda_micron**2
        * (
            (b1 * c1) / (c1 - lambda_micron**2) ** 2
            + (b2 * c2) / (c2 - lambda_micron**2) ** 2
            + (b3 * c3) / (c3 - lambda_micron**2) ** 2
        )
        ** 2
        + 2
        * (
            1
            + (b1 * lambda_micron**2) / (-c1 + lambda_micron**2)
            + (b2 * lambda_micron**2) / (-c2 + lambda_micron**2)
            + (b3 * lambda_micron**2) / (-c3 + lambda_micron**2)
        )
        * (
            (-2 * b1 * c1 * (c1 + 3 * lambda_micron**2))
            / (c1 - lambda_micron**2) ** 3
            - (2 * b2 * c2 * (c2 + 3 * lambda_micron**2))
            / (c2 - lambda_micron**2) ** 3
            - (2 * b3 * c3 * (c3 + 3 * lambda_micron**2))
            / (c3 - lambda_micron**2) ** 3
        )
    ) / (
        4.0
        * (
            1
            + (b1 * lambda_micron**2) / (-c1 + lambda_micron**2)
            + (b2 * lambda_micron**2) / (-c2 + lambda_micron**2)
            + (b3 * lambda_micron**2) / (-c3 + lambda_micron**2)
        )
        ** 1.5
    )


def two_term_serllmier(
    lambda_micron: float, b1: float, c1: float, b2: float, c2: float
) -> float:
    r"""
    :math:`n^2 -1 = \frac{B1 \lambda^2}{\lambda^2 - C1}
    + \frac{c \lambda^2}{\lambda^2 - d}`


    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    b1: float
        Coefficient B_1
    c1: float
        Coefficient C_1
    b2: float
        Coefficient B_2
    c2: float
        Coefficient C_2

    Returns
    -------
    float
        Calculated refractive index
    """
    return three_term_sellmier(lambda_micron, b1, c1, b2, c2, 0, 0)


def second_derivative_two_term_sellmier(
    lambda_micron: float, b1: float, c1: float, b2: float, c2: float
) -> float:
    """Second derivative of the two term sellmier equation

    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    b1: float
        Coefficient B_1
    c1: float
        Coefficient C_1
    b2: float
        Coefficient B_2
    c2: float
        Coefficient C_2

    Returns
    -------
    float
        Calculated refractive index
    """

    return second_derivative_three_term_sellmier(lambda_micron, b1, c1, b2, c2, 0, 0)


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
    b1 = 1.03961212
    c1 = 0.00600069867
    b2 = 0.231792344
    c2 = 0.0200179144
    b3 = 1.01046945
    c3 = 103.560653
    if second_derivative:
        return second_derivative_three_term_sellmier(
            lambda_micron, b1, c1, b2, c2, b3, c3
        )
    return three_term_sellmier(lambda_micron, b1, c1, b2, c2, b3, c3)


def FusedSilica(lambda_micron: float, second_derivative: bool = False) -> float:
    r"""Dispersion of Fusd Silica (0.21- 3.71 micron)

    https://refractiveindex.info/?shelf=glass&book=fused_silica&page=Malitson

    Parameters
    -----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.
    second_derivative: bool
        if True return :math:`\frac{d^2n}{d\lambda^2}`
    """
    b1 = 0.6961663
    c1 = 0.06840432
    b2 = 0.4079426
    c2 = 0.11624142
    b3 = 0.8974794
    c3 = 9.8961612
    if second_derivative:
        return second_derivative_three_term_sellmier(
            lambda_micron, b1, c1, b2, c2, b3, c3
        )
    return three_term_sellmier(lambda_micron, b1, c1, b2, c2, b3, c3)


def caf2(lambda_micron: float, second_derivative: bool = False) -> float:
    r"""Dispersion of caf2 (0.15 - 12 micron)

    https://www.thorlabs.co.jp/newgrouppage9.cfm?objectgroup_id=6973&tabname=UV溶融石英(UVFS)

    Parameters
    -----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.
    second_derivative: bool
        if True return :math:`\frac{d^2n}{d\lambda^2}`
    """
    b1 = 0.69913
    c1 = 0.09374
    b2 = 0.11994
    c2 = 21.18
    b3 = 4.35181
    c3 = 38.46
    if second_derivative:
        return second_derivative_three_term_sellmier(
            lambda_micron, b1, c1, b2, c2, b3, c3
        )
    return np.sqrt(
        three_term_sellmier(lambda_micron, b1, c1, b2, c2, b3, c3) ** 2 + 0.33973
    )


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
    b1 = 0.05792105
    c1 = 238.0185
    b1 = 0.00167917
    c2 = 57.362
    if second_derivative:
        return (2 * b1 * (1 + 3 * c1 * lambda_micron**2)) / (
            -1 + c1 * lambda_micron**2
        ) ** 3 + (2 * (b1 + 3 * b1 * c2 * lambda_micron**2)) / (
            -1 + c2 * lambda_micron**2
        ) ** 3
    return 1 + b1 / (c1 - lambda_micron ** (-2)) + b1 / (c2 - lambda_micron ** (-2))


def BBO_sellmeier(
    lambda_micron: float, a: float, b: float, c: float, d: float
) -> float:
    return np.sqrt(a - d * lambda_micron**2 + b / (-c + lambda_micron**2))


def BBO_sellmeier_1st_derivative(
    lambda_micron: float, a: float, b: float, c: float, d: float
) -> float:
    return -(
        (d * lambda_micron)
        / np.sqrt(a - d * lambda_micron**2 + b / (-c + lambda_micron**2))
    )


def BBO_sellmeier_2nd_derivative(
    lambda_micron: float, a: float, b: float, c: float, d: float
) -> float:
    return (d * (-a + b / (c - lambda_micron**2))) / (
        a - d * lambda_micron**2 + b / (-c + lambda_micron**2)
    ) ** (3 / 2)


def alphaBBO(
    lambda_micron: float,
    first_derivative: bool = False,
    second_derivative: bool = False,
) -> tuple[float, float]:
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

    if first_derivative:
        return (
            BBO_sellmeier_1st_derivative(
                lambda_micron, 2.67579, 0.02099, 0.00470, 0.00528
            ),
            BBO_sellmeier_1st_derivative(
                lambda_micron, 2.31197, 0.01184, 0.016070, 0.00400
            ),
        )
    if second_derivative:
        return (
            BBO_sellmeier_2nd_derivative(
                lambda_micron, 2.67579, 0.02099, 0.00470, 0.00528
            ),
            BBO_sellmeier_2nd_derivative(
                lambda_micron, 2.31197, 0.01184, 0.016070, 0.00400
            ),
        )
    return (
        BBO_sellmeier(lambda_micron, 2.67579, 0.02099, 0.00470, 0.00528),
        BBO_sellmeier(lambda_micron, 2.31197, 0.01184, 0.016070, 0.00400),
    )


def betaBBO(
    lambda_micron: float,
    first_derivative: bool = False,
    second_derivative: bool = False,
) -> tuple[float, float]:
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
    if first_derivative:
        return (
            BBO_sellmeier_1st_derivative(
                lambda_micron, 2.7359, 0.01878, 0.01822, 0.01354
            ),
            BBO_sellmeier_1st_derivative(
                lambda_micron, 2.3753, 0.01224, 0.01667, 0.01516
            ),
        )
    if second_derivative:
        return (
            BBO_sellmeier_2nd_derivative(
                lambda_micron, 2.7359, 0.01878, 0.01822, 0.01354
            ),
            BBO_sellmeier_2nd_derivative(
                lambda_micron, 2.3753, 0.01224, 0.01667, 0.01516
            ),
        )
    return (
        BBO_sellmeier(lambda_micron, 2.7359, 0.01878, 0.01822, 0.01354),
        BBO_sellmeier(lambda_micron, 2.3753, 0.01224, 0.01667, 0.01516),
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
    r"""Dispersion of mgf2

    Parameters
    ----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.

    Returns
    --------
    tuple:
        :math:`n_o` and :math:`n_e`
    """
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
