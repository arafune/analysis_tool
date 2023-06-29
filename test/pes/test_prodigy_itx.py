"""Unit test for prodigy_itx.py."""

from pathlib import Path

import numpy as np
import pytest
import xarray as xr

from pes.prodigy_itx import ProdigyItx, load_sp2

data_dir = Path(__file__).parent / "data"


@pytest.fixture()
def sample_itx() -> ProdigyItx:
    """Fixture."""
    return ProdigyItx(data_dir / "PES_16_Spectrum_3.itx")


@pytest.fixture()
def sample_sp2() -> xr.DataArray:
    """Fixture: produce xr.DataArray."""
    return load_sp2(data_dir / "GrIr_111_20230410_1.sp2")


class TestItx:
    """test Class for prodigy_itx.py."""

    def test_parameters(self, sample_itx: ProdigyItx) -> None:
        """Test for reading itx file."""
        workfunction_analyzer = 4.401
        assert sample_itx.params["WorkFunction"] == workfunction_analyzer
        assert sample_itx.pixels == (600, 501)

    def test_integrated_intensity(self, sample_itx: ProdigyItx) -> None:
        """Test for integrated_intensity property."""
        np.testing.assert_almost_equal(sample_itx.integrated_intensity, 666371.3147352)

    def test_convert_to_dataarray(self, sample_itx: ProdigyItx) -> None:
        """Test for convert to xr.DataArray."""
        sample_dataarray = sample_itx.to_data_array()
        assert sample_dataarray.dims == ("phi", "eV")


class TestSp2:
    """Test class for load_sp2 function."""

    def test_parameters(self, sample_sp2: xr.DataArray) -> None:
        assert sample_sp2.dims == ("phi", "eV")
