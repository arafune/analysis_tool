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


def ch_calib(
    data: xr.DataArray,
    offset_stride: float,
    *,
    sums: bool = True,
) -> xr.Dataset | xr.DataArray:
    """Recalibrate channels along the phi direction.

    This function shifts each cycle in the data by a specified stride and optionally
    sums the results.

    Args:
        data (xr.DataArray): The dataarray to be corrected. Must be 3-dimensional and
            contain 'cycle' coordinate.
        offset_stride (float): The value for shift along phi direction. In SPL95, the
            value is 0.09565217391304348 degrees.
        sums (bool, optional): If True, sum the recalibrated data arrays. If False,
            return concatenated arrays. Defaults to True.

    Returns:
        xr.Dataset | xr.DataArray: Calibrated ARPES data, either summed or concatenated
            by cycle.

    """
    assert data.ndim == 3
    original_attrs = data.attrs
    dict_data_array = {
        f"idx{int(_.item())}": data.sel({"cycle": _}, drop=True).assign_attrs(
            tmp_cycle=int(_.item())
        )
        for _ in data.coords["cycle"]
    }

    ds_dict = {}
    for idx, da in dict_data_array.items():
        shift_value = (da.attrs["tmp_cycle"] - 1) * offset_stride
        tmpda: xr.DataArray = da.G.shift_by(
            np.full(len(da.coords["eV"]), shift_value),
            shift_axis="phi",
        )
        ds_dict[idx] = tmpda
    ds = xr.Dataset(ds_dict)
    if not sums:
        dsarrays = ds.data_vars.values()
        cycle_values = [da.attrs["tmp_cycle"] for da in dsarrays]
        return xr.concat(
            dsarrays,
            dim=xr.DataArray(cycle_values, dims="cycle", name="cycle"),
        )

    new_da: xr.DataArray = sum(ds.data_vars.values())
    new_da.attrs = original_attrs
    return new_da
