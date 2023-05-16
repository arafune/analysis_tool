import numpy as np


def broadening(initial_width_fs: float, gdd: float) -> float:
    """Return pulse broadening due to GDD

    Parameters
    ----------
    initial_width_fs: float
        initial pulse width (fs unit)
    gdd: float
        Group delay dispersion (fs^2/mm unit)

    Returns
    -------
    float
        the output pulse width (fs unit)
    """
    return (
        np.sqrt(initial_width_fs**4 + 16 * np.log(2) ** 2 * gdd**2)
        / initial_width_fs
    )


def gvd(lambda_micron: float, d2n: float) -> float:
    """Return gvd in fs/mm"""
    light_speed_micron_fs = 0.299792458
    return lambda_micron**3 / (2 * np.pi * light_speed_micron_fs**2) * d2n * 1e3
