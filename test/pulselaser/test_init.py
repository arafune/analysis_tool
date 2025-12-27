"""Unit test for sellmeier/__init__.py."""

import numpy as np
import pytest

import pulselaser


@pytest.mark.parametrize(
    ("material", "refractive_index"),
    [
        ("bk7", 44.651),
        ("beta_bbo", (71.864, 56.883)),
    ],
)
def test_gvd_at_800nm(material: str, refractive_index: float) -> None:
    np.testing.assert_allclose(
        pulselaser.gvd(0.800, material), refractive_index, rtol=0.0001
    )
