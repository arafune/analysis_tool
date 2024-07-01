import numpy as np

from numpy.typing import NDArray


def gaussian_envelop(
    t: NDArray[np.float64],
    fwhm: float,
    intensity: float = 1,
    t0: float = 0,
) -> NDArray[np.float64]:
    """Gaussian function defined by FWHM."""
    sigma: float = fwhm / (2.0 * np.sqrt(np.log(2.0)))
    return intensity * np.exp(-((t - t0) ** 2) / sigma**2)


def bloch(
    t: NDArray[np.float64],
    rho: NDArray[np.complex128],
    fwhm: float,
    t1: float,
    omega12_minus_omega: float,
    amplitude: float,
) -> NDArray[np.complex128]:
    """Bloch equation for two level system with a pulse excitation.

    [TODO:description]

    Parameters
    ----------
    t
        [TODO:description]
    rho
        [TODO:description]
    fwhm
        [TODO:description]
    t1
        [TODO:description]
    omega12_minus_omega
        [TODO:description]
    amplitude
        [TODO:description]

    Returns
    -------
    NDArray[np.complex128]
        [TODO:description]
    """
    e_field: NDArray[np.float64] = gaussian_envelop(
        t=t,
        fwhm=fwhm,
        intensity=1,
        t0=fwhm * 10,
    )
    t2 = 2 * t1
    r22: NDArray[np.float64] = np.real(rho[0])
    r11: NDArray[np.float64] = 1.0 - r22
    r12t: NDArray[np.complex128] = rho[1]
    r21t: NDArray[np.complex128] = np.conjugate(r12t)
    dr22dt = 1.0j * amplitude * e_field * (r12t - r21t) - r22 / t1
    dr12tdt = (
        1.0j * amplitude * e_field * (r22 - r11)
        + (1.0j * omega12_minus_omega - 1 / t2) * r12t
    )
    return np.array([dr22dt, dr12tdt])
