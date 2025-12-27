"""Unit test for pulselaser.sellmeier."""

import numpy as np
import pytest

import pulselaser.sellmeier as sellmeier
import sympy as sp


class TestAir:
    def test_at_dline(self) -> None:
        """Test for n at 587.6nm

        The value is taken from https://refractiveindex.info/?shelf=other&book=air&page=Ciddor#google_vignette
        """
        np.testing.assert_allclose(sellmeier.air(0.5876), 1.00027717)

    def test_for_negative_derivative(self):
        with pytest.raises(ValueError):
            sellmeier.air(0.5876, derivative=-1)


class TestBK7:
    def test_at_800nm(self) -> None:
        """Test for n of BK7 at 800nm ~1.5108."""
        assert sellmeier.bk7(0.80) == 1.5107762314198743

    def test_negative_derivative(self) -> None:
        with pytest.raises(
            ValueError,
            match="derivative must be equal or greater than zero",
        ):
            sellmeier.bk7(0.5876, derivative=-1)

    def test_sympy_objet(self) -> None:
        """Test for as_sympy."""
        assert isinstance(sellmeier.bk7(0.80, as_sympy=True), sp.Expr)


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


class TestMgF2:
    def test_at_dline(self) -> None:
        """Test for n of MgF2 at 586.7 nm.

        at Thorlabs web:

        * ne = 1.390
        * no = 1.378
        """
        np.testing.assert_allclose(
            sellmeier.mgf2(0.5867),
            (1.378, 1.390),
            atol=0.001,
            rtol=0.001,
        )


class TestCalcite:
    def test_at_YAG(self) -> None:  # noqa: N802
        """Test for n of Calcite at Nd:YAG laser (1.064 µm).

        in Thorlabs Web:

            * ne =  1.480
            * no = 1.642

        """
        np.testing.assert_allclose(
            sellmeier.calcite(1.064),
            (1.642, 1.480),
            atol=0.001,
            rtol=0.001,
        )


class TestQuartz:
    def test_at_800nm(self) -> None:
        assert sellmeier.quartz(0.80) == (1.5383355123424691, 1.5472301086112594)


class TestAlhpaBBO:
    def test_at_dline(self) -> None:
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


def test_phase_matching_angle_bbo_at_800() -> None:
    np.testing.assert_allclose(
        sellmeier.phase_matching_angle_bbo(0.800), 29.02, atol=0.01
    )


def test_phase_matching_angle_bbo_at_790() -> None:
    np.testing.assert_allclose(
        sellmeier.phase_matching_angle_bbo(0.790), 29.4, atol=0.01
    )
