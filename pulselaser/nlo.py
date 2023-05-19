#! /usr/bin/env python3

"""Calculate the NLO crystal characteristics"""
import argparse
from typing import Callable

import numpy as np

from pulselaser import sellmeier


def cut_angle_deg(
    input_wavelength_micron: float = 0.800,
    material: Callable[float, tuple[float, float]] = sellmeier.betaBBO,
) -> float:
    no_1: float = material(input_wavelength_micron)[0]
    ne_1: float = material(input_wavelength_micron)[1]
    no_2: float = material(input_wavelength_micron / 2)[0]
    ne_2: float = material(input_wavelength_micron / 2)[1]
    #
    return np.rad2deg(
        np.arcsin(
            np.sqrt(
                ((ne_2**2) * (no_2**2 - no_1**2))
                / ((no_1**2) * (no_2**2 - ne_2**2))
            )
        )
    )


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("lambda_micron", type=float, help="Fundamental wavelength")
    args = parser.parse_args()
    print(cut_angle_deg(args.lambda_micron))
