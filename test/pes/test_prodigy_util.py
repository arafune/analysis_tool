from pathlib import Path

import numpy as np
import pytest

from pes.prodigy_util import ProdigyItx

data_dir = Path(__file__).parent / "data"


@pytest.fixture()
def sample_itx() -> ProdigyItx:
    return ProdigyItx(data_dir / "PES_16_Spectrum_3.itx")


class TestItx:
    def test_parameters(self, sample_itx: ProdigyItx) -> None:
        assert sample_itx.params["WorkFunction"] == 4.401
        assert sample_itx.pixels == (600, 501)

    def test_integrated_intensity(self, sample_itx: ProdigyItx) -> None:
        np.testing.assert_almost_equal(sample_itx.integrated_intensity, 666371.3147352)
