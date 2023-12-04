import numpy as np


def sech2(x: float, x0: float, width: float) -> float:
    r"""Return :math:`\mathrm{sech}^2\left(\frac{x-x0}{\tau}\right)`.

    .. note::

    This function does not include the amplitude.

    Parameters
    ----------
    x: float
        x
    x0: float
        center position
    width: float
        width of the function :math:`\tau`. Not FWHM. (FWHM= :math:`1.7627 \tau` )

    Returns
    -------
    float
    """
    return (1 / np.cosh((x - x0) / width)) ** 2


def broadening(initial_width_fs: float, gdd: float) -> float:
    """Return pulse broadening due to GDD.

    Parameters
    ----------
    initial_width_fs: float
        initial pulse width (fs unit)
    gdd: float
        Group delay dispersion (fs^2 unit)

    Returns
    -------
    float
        the output pulse width (fs unit)
    """
    assert initial_width_fs > 0
    assert gdd > 0
    return (
        np.sqrt(initial_width_fs**4 + (gdd**2) * 16 * np.log(2) ** 2) / initial_width_fs
    )


def broadening_after_n(
    initial_width_fs: float,
    gdd: float,
    iteration: int = 1,
) -> float:
    """Return pulse broadening due to GDD after N iteration.

    Parameters
    ----------
    initial_width_fs: float
        initial pulse width (fs unit)
    gdd: float
        Group delay dispersion (fs^2 unit)
    iteration: int
        Number of iteration

    Returns
    -------
    float
        the output pulse width (fs unit)
    """
    assert isinstance(iteration, int)
    assert iteration > 0
    if iteration == 1:
        return broadening(initial_width_fs, gdd)
    return broadening(broadening_after_n(initial_width_fs, gdd, iteration - 1), gdd)


def gdd(input_pulse_duration_fs: float, output_pulse_duration_fs: float) -> float:
    """Return the GDD value of the optics.

    Parameters
    ----------
    input_pulse_duration_fs: float
        The duration of the input pulse
    output_pulse_duration_fs: float
        The duration of the output pulse

    Returns
    -------
    float
        GDD value
    """
    return (
        np.sqrt(output_pulse_duration_fs**2 - input_pulse_duration_fs**2)
        * input_pulse_duration_fs
        / (4 * np.log(2))
    )


def gvd(lambda_micron: float, d2n: float) -> float:
    """Return GVD in fs^2/mm units."""
    light_speed_micron_fs = 0.299792458
    return lambda_micron**3 / (2 * np.pi * light_speed_micron_fs**2) * d2n * 1e3
