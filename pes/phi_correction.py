"""Helper Function for phi correction.

"import arpes" is essentially required.
"""

from collections.abc import Callable
from typing import TypeVar

import numpy as np
import xarray as xr
from numpy.typing import NDArray

T = TypeVar("T", NDArray[np.float64], float, xr.DataArray)


def phi_shift_from_pes130(energy: T) -> T:
    """Return the corrected phi value based on the energy.

    Based on the results of PES_130 (sample: Cu(001))
    """
    best_values = {
        "a": np.float64(0.021659247779521107),
        "b": np.float64(-0.19962481847388602),
    }
    return best_values["a"] * energy + best_values["b"]


def correct_phi(
    data: xr.DataArray,
    phi_shift_func: Callable[[float], float] = phi_shift_from_pes130,
    shurink_phi: float = 0.73,
) -> xr.DataArray:
    """Return the corrected phi data.

    Args:
        data: The data to be corrected.
        phi_shift_func: The function to calculate the phi shift.
        shurink_phi: The factor to shrink the phi shift.

    Returns:
        The corrected phi data.

    """
    correction: xr.DataArray = phi_shift_func(data.coords["eV"])
    shifted: xr.DataArray = data.G.shift_by(correction, "phi", extend_coords=True)
    return shifted.assign_coords(phi=shifted.phi * shurink_phi).dropna(
        dim="phi",
        how="all",
    )
