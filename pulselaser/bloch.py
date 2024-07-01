import numpy as np
from numpy.typing import NDArray


def gaussian_envelope(
    t: NDArray[np.float64],
    fwhm: float,
    intensity: float = 1,
    t0: float = 0,
) -> NDArray[np.float64]:
    """Gaussian function defined by FWHM.

    The height (not the area) can be set.

    Parameters
    ----------
    t: NDArray[np.float64]
        time
    fwhm: float
        Full width at half maximum.
    intensity: float
        The height of the pulse.[TODO:description
    t0: float
        The center offset.

    Returns
    -------
    NDArray[np.float64]
        [TODO:description]

    """
    sigma: float = fwhm / (2.0 * np.sqrt(np.log(2.0)))
    return intensity * np.exp(-((t - t0) ** 2) / sigma**2)


def bloch(  # noqa: PLR0913
    t: NDArray[np.float64],
    rho: NDArray[np.complex128],
    fwhm: float,
    t1: float,
    omega12_minus_omega: float,
    amplitude: float,
) -> NDArray[np.complex128]:
    r"""Bloch equation for two level system with a pulse excitation.

    Parameters
    ----------
    t
        time in fs unit.
    rho
        :math:`\rho_{22}` and :math:`\tilde{\rho}_{12}`:
            Note that :math:`\rho_{22}` is real, :math:`\tilde{\rho}_{12}` is complex.
    fwhm
        FWHM of input pluse.
    t1
        Population decay time (:math:`T_1`).  The Dephasing time (:math:`T_2` is assumed
        as :math:`2T_1`  (The pure dephasing time is assumed as infinity.)
    omega12_minus_omega
        :math:`\omega_{12}-\omega`, 0 means the resonant condition, while !=0 is off
        resonant.
    amplitude
        [TODO:description]

    Returns
    -------
    NDArray[np.complex128]
        :math:`\frac{d\rho_{22}}{dt}` and :math:`\frac{d\tilde{\rho}_{12}}{dt}`

    """
    e_field: NDArray[np.float64] = gaussian_envelope(
        t=t,
        fwhm=fwhm,
        intensity=1,
        t0=300,
    )
    t2 = 2 * t1
    r22: NDArray[np.float64] = np.real(rho[0])
    r11: NDArray[np.float64] = 1.0 - r22
    r12t: NDArray[np.complex128] = rho[1]
    r21t: NDArray[np.complex128] = np.conjugate(r12t)
    dr22dt = -1.0j * amplitude * e_field * (r12t - r21t) - r22 / t1
    dr12tdt = (
        -1.0j * amplitude * e_field * (r22 - r11)
        + (1.0j * omega12_minus_omega - 1 / t2) * r12t
    )
    return np.array([dr22dt, dr12tdt])
