#! /usr/bin/env python3

import pulselaser.sellmeier as sellmeier


class TestBK7:
    def test_at_800nm(self) -> None:
        assert sellmeier.bk7(0.80) == 1.5071655107493938


class TestFusedSilica:
    def test_at_800nm(self) -> None:
        assert sellmeier.fused_silica(0.80) == 1.4533172570445876


class TestCaF2:
    def test_at_800nm(self) -> None:
        assert sellmeier.caf2(0.80) == 1.4305724647561817


class TestSF10:
    def test_at_800nm(self) -> None:
        assert sellmeier.sf10(0.80) == 1.696934373227597


class TestQuartz:
    def test_at_800nm(self) -> None:
        assert sellmeier.quartz(0.80) == (1.5383355123424691, 1.5472301086112594)


class TestAlhpaBBO:
    def test_at_800nm(self) -> None:
        assert sellmeier.alpha_bbo(0.800) == (1.6448253125768209, 1.52590513720448)

    def test_at_400nm(self) -> None:
        assert sellmeier.alpha_bbo(0.400) == (1.676336171290171, 1.5471238511499055)


class TestBetaBBO:
    def test_at_800nm(self) -> None:
        assert sellmeier.beta_bbo(0.800) == (1.660553524880645, 1.5444203018104292)

    def test_at_400nm(self) -> None:
        assert sellmeier.beta_bbo(0.400) == (1.6929832659808661, 1.5678876665187913)
