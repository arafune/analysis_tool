import numpy as np

from numpy.typing import NDArray


def gaussian_envelop(
    t: NDArray[np.float64],
    fwhm: float,
    intensity: float = 1,
    t0: float = 0,
) -> NDArray[np.float64]:
    """Gaussian function defined by FWHM."""
    sigma: float = fwhm / (2 * np.sqrt(np.log(2)))
    return intensity * np.exp(-((t - t0) ** 2) / sigma**2)
