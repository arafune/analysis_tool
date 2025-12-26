"""Unit test for pulselaser.sellmeier."""

import numpy as np

import pulselaser.sellmeier as sellmeier


class TestBK7:
    def test_at_800nm(self) -> None:
        """Test for n of BK7 at 800nm ~1.5108."""
        assert sellmeier.bk7(0.80) == 1.5107762314198743


class TestFusedSilica:
    def test_at_800nm(self) -> None:
        """Test for n of FusedSilica at 800nm ~1.4533."""
        assert sellmeier.fused_silica(0.80) == 1.4533172570445876


class TestCaF2:
    def test_at_800nm(self) -> None:
        assert sellmeier.caf2(0.80) == 1.4305724647561817


class TestSF10:
    def test_at_800nm(self) -> None:
        """Test for n of SF10 at 800nm ~1.7113."""
        np.testing.assert_allclose(
            sellmeier.sf10(0.80),
            1.7112,
            atol=0.001,
            rtol=0.001,
        )


class TestQuartz:
    def test_at_800nm(self) -> None:
        assert sellmeier.quartz(0.80) == (1.5383355123424691, 1.5472301086112594)


class TestAlhpaBBO:
    def test_at_587p6(self) -> None:
        np.testing.assert_allclose(
            sellmeier.alpha_bbo(0.5876),
            (1.673, 1.533),
            rtol=0.001,
            atol=0.001,
        )


class TestBetaBBO:
    def test_at_800nm(self) -> None:
        np.testing.assert_allclose(
            sellmeier.beta_bbo(0.800),
            (1.6614, 1.5462),
            atol=0.001,
            rtol=0.001,
        )
