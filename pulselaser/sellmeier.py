"""Collection of Sellmeier equation."""

from __future__ import annotations

import numpy as np

from typing import Literal

DERIVATIVE_ORDER = Literal[0, 1, 2]


def three_term_sellmier(
    lambda_micron: float,
    coeff_b: tuple[float, float, float],
    coeff_c: tuple[float, float, float],
) -> float:
    r"""Return Sellmeier function.

    :math:`n^2 -1 = \frac{B_1 \lambda^2}{\lambda^2 - C_1} +
    \frac{B_2 \lambda^2}{\lambda^2 - C_2} + \frac{B_3 \lambda^2}{\lambda^2 - C_3}`.


    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    coeff_b: tuple[float, float, float]
        Coefficient B
    coeff_c: tuple[float, float, float]
        Coefficient C

    Returns
    -------
    float
        Calculated refractive index
    """
    b1, b2, b3 = coeff_b
    c1, c2, c3 = coeff_c
    n2 = (
        1
        + b1 * lambda_micron**2 / (lambda_micron**2 - c1**2)
        + b2 * lambda_micron**2 / (lambda_micron**2 - c2**2)
        + b3 * lambda_micron**2 / (lambda_micron**2 - c3**2)
    )
    return np.sqrt(n2)


def first_derivative_three_term_sellmier(
    lambda_micron: float,
    coeff_b: tuple[float, float, float],
    coeff_c: tuple[float, float, float],
) -> float:
    r"""Return the first derivative of Sellmeier function.

    :math:`n^2 -1 = \frac{B_1 \lambda^2}{\lambda^2 - C_1} +
    \frac{B_2 \lambda^2}{\lambda^2 - C_2} + \frac{B_3 \lambda^2}{\lambda^2 - C_3}`.


    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    coeff_b: tuple[float, float, float]
        Coefficient B
    coeff_c: tuple[float, float, float]
        Coefficient C

    Returns
    -------
    float
        Calculated refractive index
    """
    b1, b2, b3 = coeff_b
    c1, c2, c3 = coeff_c
    return (
        lambda_micron
        * (
            (b1 * (-2 * c1**2 + lambda_micron)) / (c1**2 - lambda_micron) ** 2
            + (b2 * (-2 * c2**2 + lambda_micron)) / (c2**2 - lambda_micron) ** 2
            + (b3 * (-2 * c3**2 + lambda_micron)) / (c3**2 - lambda_micron) ** 2
        )
    ) / (
        2.0
        * np.sqrt(
            1
            + (b1 * lambda_micron**2) / (-(c1**2) + lambda_micron)
            + (b2 * lambda_micron**2) / (-(c2**2) + lambda_micron)
            + (b3 * lambda_micron**2) / (-(c3**2) + lambda_micron),
        )
    )


def second_derivative_three_term_sellmier(
    lambda_micron: float,
    coeff_b: tuple[float, float, float],
    coeff_c: tuple[float, float, float],
) -> float:
    """Second derivative of the three term sellmier equation.

    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    coeff_b: tuple[float, float, float]
        Coefficient B
    coeff_c: tuple[float, float, float]
        Coefficient C

    Returns
    -------
    float
        Calculated refractive index
    """
    b1, b2, b3 = coeff_b
    c1, c2, c3 = coeff_c
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
            (-2 * b1 * c1 * (c1 + 3 * lambda_micron**2)) / (c1 - lambda_micron**2) ** 3
            - (2 * b2 * c2 * (c2 + 3 * lambda_micron**2)) / (c2 - lambda_micron**2) ** 3
            - (2 * b3 * c3 * (c3 + 3 * lambda_micron**2)) / (c3 - lambda_micron**2) ** 3
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
    lambda_micron: float,
    coeff_b: tuple[float, float],
    coeff_c: tuple[float, float],
) -> float:
    r"""Return the Sellmeier function represented by two terms.

    :math:`n^2 -1 = \frac{B_1 \lambda^2}{\lambda^2 - C_1} +
    \frac{B_2 \lambda^2}{\lambda^2 - C_2}`.

    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    coeff_b: tuple[float, float]
        Coefficient B
    coeff_c: tuple[float, float]
        Coefficient C

    Returns
    -------
    float
        Calculated refractive index
    """
    return three_term_sellmier(
        lambda_micron,
        (*coeff_b, 0),
        (*coeff_c, 0),
    )


def first_derivative_two_term_sellmier(
    lambda_micron: float,
    coeff_b: tuple[float, float],
    coeff_c: tuple[float, float],
) -> float:
    """First derivative of the two term sellmier equation.

    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    coeff_b: tuple[float, float]
        Coefficient B
    coeff_c: tuple[float, float]
        Coefficient C

    Returns
    -------
    float
        Calculated refractive index
    """
    return first_derivative_three_term_sellmier(
        lambda_micron,
        (*coeff_b, 0),
        (*coeff_c, 0),
    )


def second_derivative_two_term_sellmier(
    lambda_micron: float,
    coeff_b: tuple[float, float],
    coeff_c: tuple[float, float],
) -> float:
    """Second derivative of the two term sellmier equation.

    Parameters
    ----------
    lambda_micron: float
        wavelength in micron
    coeff_b: tuple[float, float]
        Coefficient B
    coeff_c: tuple[float, float]
        Coefficient C

    Returns
    -------
    float
        Calculated refractive index
    """
    return second_derivative_three_term_sellmier(
        lambda_micron,
        (*coeff_b, 0),
        (*coeff_c, 0),
    )


# -----------


def bk7(lambda_micron: float, *, derivative: DERIVATIVE_ORDER = 0) -> float:
    r"""Dispersion of BK7.

    https://refractiveindex.info/?shelf=glass&book=BK7&page=SCHOTT

    Parameters
    ----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.
    second_derivative: bool
        if True return :math:`\frac{d^2n}{d\lambda^2}`
    """
    b = (1.03961212, 0.231792344, 1.01046945)
    c = (np.sqrt(0.00600069867), np.sqrt(0.0200179144), np.sqrt(103.560653))
    if derivative == 0:
        return three_term_sellmier(lambda_micron, b, c)
    if derivative == 1:
        return first_derivative_three_term_sellmier(lambda_micron, b, c)
    if derivative == 2:
        return second_derivative_three_term_sellmier(
            lambda_micron,
            b,
            c,
        )
    msg = "Derivative order should be 0, 1, or 2"
    raise RuntimeError(msg)


def fused_silica(lambda_micron: float, *, derivative: DERIVATIVE_ORDER = 0) -> float:
    r"""Dispersion of Fusd Silica (0.21- 3.71 micron).

    https://refractiveindex.info/?shelf=glass&book=fused_silica&page=Malitson

    Parameters
    ----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.
    second_derivative: bool
        if True return :math:`\frac{d^2n}{d\lambda^2}`
    """
    b = (0.6961663, 0.4079426, 0.8974794)
    c = (0.06840432, 0.11624142, 9.8961612)
    if derivative == 0:
        return three_term_sellmier(lambda_micron, b, c)
    if derivative == 1:
        return first_derivative_three_term_sellmier(lambda_micron, b, c)
    if derivative == 2:
        return second_derivative_three_term_sellmier(
            lambda_micron,
            b,
            c,
        )
    msg = "Derivative order should be 0, 1, or 2"
    raise RuntimeError(msg)


def caf2(lambda_micron: float, *, derivative: DERIVATIVE_ORDER = 0) -> float:
    r"""Dispersion of caf2 (0.15 - 12 micron).

    Parameters
    ----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.
    second_derivative: bool
        if True return :math:`\frac{d^2n}{d\lambda^2}`
    """
    b = (0.69913, 0.11994, 4.35181)
    c = (0.09374, 21.18, 38.46)
    if derivative == 0:
        return np.sqrt(
            three_term_sellmier(lambda_micron, b, c) ** 2 + 0.33973,
        )
    if derivative == 1:
        return first_derivative_three_term_sellmier(lambda_micron, b, c)
    if derivative == 2:
        return second_derivative_three_term_sellmier(
            lambda_micron,
            b,
            c,
        )
    msg = "Derivative order should be 0, 1, or 2"
    raise RuntimeError(msg)


def sf10(lambda_micron: float, *, derivative: DERIVATIVE_ORDER = 0) -> float:
    r"""Dispersion of SF10 (0.15 - 12 micron).

    https://refractiveindex.info/?shelf=glass&book=SF10&page=SCHOTT

    Parameters
    ----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.
    second_derivative: bool
        if True return :math:`\frac{d^2n}{d\lambda^2}`
    """
    b = (1.6215390, 0.256287842, 1.64447552)
    c = (np.sqrt(0.0122241457), np.sqrt(0.0595736775), np.sqrt(147.468793))
    if derivative == 0:
        return three_term_sellmier(lambda_micron, b, c)
    if derivative == 1:
        return first_derivative_three_term_sellmier(lambda_micron, b, c)
    if derivative == 2:
        return second_derivative_three_term_sellmier(
            lambda_micron,
            b,
            c,
        )
    msg = "Derivative order should be 0, 1, or 2"
    raise RuntimeError(msg)


def air(lambda_micron: float, *, second_derivative: bool = False) -> float:
    r"""Dispersion of air.

    https://refractiveindelambda_micron.info/?shelf=other&book=air&page=Ciddor

    Parameters
    ----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.
    second_derivative: bool
        if True return :math:`\frac{d^2n}{d\lambda^2}`

    Returns
    -------
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


def bbo_sellmeier(
    lambda_micron: float,
    a: float,
    b: float,
    c: float,
    d: float,
) -> float:
    return np.sqrt(a - d * lambda_micron**2 + b / (-c + lambda_micron**2))


def bbo_sellmeier_1st_derivative(
    lambda_micron: float,
    a: float,
    b: float,
    c: float,
    d: float,
) -> float:
    return -(
        (d * lambda_micron)
        / np.sqrt(a - d * lambda_micron**2 + b / (-c + lambda_micron**2))
    )


def bbo_sellmeier_2nd_derivative(
    lambda_micron: float,
    a: float,
    b: float,
    c: float,
    d: float,
) -> float:
    return (d * (-a + b / (c - lambda_micron**2))) / (
        a - d * lambda_micron**2 + b / (-c + lambda_micron**2)
    ) ** (3 / 2)


def alpha_bbo(
    lambda_micron: float,
    *,
    first_derivative: bool = False,
    second_derivative: bool = False,
) -> tuple[float, float]:
    r"""Dispersion of :math:`\alpha`-BBO.

    http://www.newlightphotonics.com/Birefringent-Crystals/alpha-BBO-Crystals


    * Negative birefringence

    Parameters
    ----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.

    Return
    -------
    tuple:
        :math:`n_o` and :math:`n_e`
    """
    if first_derivative:
        return (
            bbo_sellmeier_1st_derivative(
                lambda_micron,
                2.67579,
                0.02099,
                0.00470,
                0.00528,
            ),
            bbo_sellmeier_1st_derivative(
                lambda_micron,
                2.31197,
                0.01184,
                0.016070,
                0.00400,
            ),
        )
    if second_derivative:
        return (
            bbo_sellmeier_2nd_derivative(
                lambda_micron,
                2.67579,
                0.02099,
                0.00470,
                0.00528,
            ),
            bbo_sellmeier_2nd_derivative(
                lambda_micron,
                2.31197,
                0.01184,
                0.016070,
                0.00400,
            ),
        )
    return (
        bbo_sellmeier(lambda_micron, 2.67579, 0.02099, 0.00470, 0.00528),
        bbo_sellmeier(lambda_micron, 2.31197, 0.01184, 0.016070, 0.00400),
    )


def beta_bbo(
    lambda_micron: float,
    *,
    first_derivative: bool = False,
    second_derivative: bool = False,
) -> tuple[float, float]:
    r"""Return :math:`n_o` and :math:`n_e` of :math:`\beta`-BBO.

    http://www.castech.com/manage/upfile/fileload/20170823144544.pdf

    * Negative birefringence

    Parameters
    ----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.

    Returns
    -------
    tuple:
        :math:`n_o` and :math:`n_e`

    """
    if first_derivative:
        return (
            bbo_sellmeier_1st_derivative(
                lambda_micron,
                2.7359,
                0.01878,
                0.01822,
                0.01354,
            ),
            bbo_sellmeier_1st_derivative(
                lambda_micron,
                2.3753,
                0.01224,
                0.01667,
                0.01516,
            ),
        )
    if second_derivative:
        return (
            bbo_sellmeier_2nd_derivative(
                lambda_micron,
                2.7359,
                0.01878,
                0.01822,
                0.01354,
            ),
            bbo_sellmeier_2nd_derivative(
                lambda_micron,
                2.3753,
                0.01224,
                0.01667,
                0.01516,
            ),
        )
    return (
        bbo_sellmeier(lambda_micron, 2.7359, 0.01878, 0.01822, 0.01354),
        bbo_sellmeier(lambda_micron, 2.3753, 0.01224, 0.01667, 0.01516),
    )


def quartz(lambda_micron: float) -> tuple[float, float]:
    r"""Dispersion of crystal quartz.

    Optics communications. 2011, vol. 284, issue 12, p. 2683-2686.

    Parameters
    ----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.

    Returns
    -------
    tuple:
        :math:`n_o` and :math:`n_e`

    """
    return (
        np.sqrt(
            1.28604141
            + 1.07044083 * lambda_micron**2 / (lambda_micron**2 - 1.00585997 * 1e-2)
            + 1.10202242 * lambda_micron**2 / (lambda_micron**2 - 100),
        ),
        np.sqrt(
            1.28851804
            + 1.09509924 * lambda_micron**2 / (lambda_micron**2 - 1.02101864 * 1e-2)
            + 1.15662475 * lambda_micron**2 / (lambda_micron**2 - 100),
        ),
    )


def calcite(lambda_micron: float) -> tuple[float, float]:
    r"""Dispersion of calcite.  (:math:`\mathrm{CaCO}_3`).

    http://www.redoptronics.com/Calcite-crystal.html

    * Negative birefringence

    Parameters
    ----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.

    Returns
    -------
    tuple:
        :math:`n_o` and :math:`n_e`

    """
    return (
        np.sqrt(
            1.28604141
            + 1.07044083 * lambda_micron**2 / (lambda_micron**2 - 1.00585997 * 1e-2)
            + 1.10202242 * lambda_micron**2 / (lambda_micron**2 - 100),
        ),
        np.sqrt(
            1.28851804
            + 1.09509924 * lambda_micron**2 / (lambda_micron**2 - 1.02101864 * 1e-2)
            + 1.15662475 * lambda_micron**2 / (lambda_micron**2 - 100),
        ),
    )


def mgf2(lambda_micron: float) -> tuple[float, float]:
    r"""Dispersion of mgf2.

    Parameters
    ----------
    lambda_micron: float
        wavelength (:math:`\lambda`) in micron (:math:`\mu m`) unit.

    Returns
    -------
    tuple:
        :math:`n_o` and :math:`n_e`
    """
    no = np.sqrt(
        1
        + 0.4876 * lambda_micron**2 / (lambda_micron**2 - 0.0434**2)
        + 0.3988 * lambda_micron**2 / (lambda_micron**2 - 0.0946**2)
        + 2.3120 * lambda_micron**2 / (lambda_micron**2 - 23.7936**2),
    )
    ne = np.sqrt(
        1
        + 0.4134 * lambda_micron**2 / (lambda_micron**2 - 0.0368**2)
        + 0.5050 * lambda_micron**2 / (lambda_micron**2 - 0.0908**2)
        + 2.4905 * lambda_micron**2 / (lambda_micron**2 - 23.7720**2),
    )
    return (no, ne)


def phase_matching_angle_bbo(fundamental_micron: float) -> float:
    """Phase matching angle of beta-BBO for SHG.

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
        (beta_bbo(fundamental_micron)[0]) ** (-2)
        - (beta_bbo(fundamental_micron / 2)[0] ** (-2))
    ) / (
        (beta_bbo(fundamental_micron / 2)[1]) ** (-2)
        - (beta_bbo(fundamental_micron / 2)[0] ** (-2))
    )
    return np.rad2deg(np.arcsin(np.sqrt(sin2theta)))
