"""Implements loading the itx and sp2 text file format for SPECS prodigy."""
import warnings
from pathlib import Path

import numpy as np

import xarray as xr
from arpes.endstations import HemisphericalEndstation, add_endstation
from arpes.utilities import clean_keys
import arpes.xarray_extensions
from pes.prodigy_util import load_itx, load_sp2


__all__ = [
    "SPDEndstation",
]


class SPDEndstation(HemisphericalEndstation):
    """Implements itx and sp2 files from the Prodigy.

    Parameters
    ----------
    HemisphericalEndstation : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    PRINCIPAL_NAME = "SPD"
    ALIASES = [
        "SPD_phoibos",
    ]
    _TOLERATED_EXTENSIONS = {".itx", ".sp2"}

    RENAME_KEYS = {
        # "itxやsp2で使われている名前": "pyarpes で使う名前",
    }

    MERGE_ATTRS = {
        "analyzer": "Specs PHOIBOS 100",
        "analyzer_name": "Specs PHOIBOS 100",
        "parallel_deflectors": False,
        "perpendicular_deflectors": False,
        "analyzer_radius": 100,
        "analyzer_type": "hemispherical",
        "mcp_voltage": None,
    }

    # def resolve_frame_locations(self, scan_desc: dict = None): ## 多分いらない。
    #     """There is only a single file for the MBS loader, so this is simple."""
    #     return [scan_desc.get("path", scan_desc.get("file"))]

    # def postprocess_final(self, data: xr.Dataset, scan_desc: dict = None): ## 多分要らない
    #    """Performs final data normalization.
    #
    #    Because the MBS format does not come from a proper ARPES DAQ setup,
    #    we have to attach a bunch of missing coordinates with blank values
    #    in order to fit the data model.
    #    """
    #    warnings.warn(
    #        "Loading from text format misses metadata. You will need to supply "
    #        "missing coordinates as appropriate."
    #    )
    #    data.attrs["psi"] = float(data.attrs["psi"])
    #    for s in data.S.spectra:
    #        s.attrs["psi"] = float(s.attrs["psi"])
    #
    #    defaults = {
    #        "x": np.nan,
    #        "y": np.nan,
    #        "z": np.nan,
    #        "theta": 0,
    #        "beta": 0,
    #        "chi": 0,
    #        "alpha": np.nan,
    #        "hv": np.nan,
    #    }
    #    for k, v in defaults.items():
    #        data.attrs[k] = v
    #        for s in data.S.spectra:
    #            s.attrs[k] = v
    #
    #    return super().postprocess_final(data, scan_desc)

    def load_single_frame(
        self, frame_path: str = None, scan_desc: dict = None, **kwargs
    ) -> xr.Dataset:
        """Load a single frame from an PHOIBOS 100 spectrometer with Prodigy.

        Parameters
        ----------
        frame_path : str, optional
            _description_, by default None
        scan_desc : dict, optional
            _description_, by default None

        Returns
        -------
        xr.Dataset
            _description_
        """
        file = Path(frame_path)

        if file.suffix == ".itx":
            data: xr.DataArray = load_itx(frame_path)
            return xr.Dataset({"spectrum": data}, attrs=data.attrs)
        elif file.suffix == ".sp2":
            data: xr.DataArray = load_sp2(frame_path)
            return xr.Dataset({"spectrum": data}, attrs=data.attrs)


add_endstation(SPDEndstation)
