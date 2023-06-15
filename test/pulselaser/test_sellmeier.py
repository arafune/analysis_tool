#! /usr/bin/env python3

import numpy as np
import pytest

import pulselaser.sellmeier as sellmeier


class Test_alhpaBBO:
    def test_at_800nm(self) -> None:
        assert sellmeier.alphaBBO(0.800) == (1.6448253125768209, 1.52590513720448)

    def test_at_400nm(self) -> None:
        assert sellmeier.alphaBBO(0.400) == (1.676336171290171, 1.5471238511499055)


class Test_betaBBO:
    def test_at_800nm(self) -> None:
        assert sellmeier.betaBBO(0.800) == (1.660553524880645, 1.5444203018104292)

    def test_at_400nm(self) -> None:
        assert sellmeier.betaBBO(0.400) == (1.6929832659808661, 1.5678876665187913)
