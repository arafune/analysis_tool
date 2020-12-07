#!/usr/bin/env python3

"""Module for analyzing the CePc2 on monolayer CePc2 on Au(111) vasp calculation
Code for vasp calculation results requested by Prof. Komeda (Nov, 2020)

(2x2) 
"""

from double_decker import two_by_two as two_by_two
from typing import Dict, List

DIFF_FROM_SERIES_INDEX: Dict[str, int] = {
    "C": -1,
    "H": 319,  # <- 255
    "N": 479,  # <- 383
    "Ce": 559,
    "Tb": 559,
    "Au": 564,
}


molecule1: Dict[str, List[int]] = two_by_two.molecule1
molecule2: Dict[str, List[int]] = two_by_two.molecule2
molecule3: Dict[str, List[int]] = two_by_two.molecule3
molecule4: Dict[str, List[int]] = two_by_two.molecule4
molecule5: Dict[str, List[int]] = {
    "C_low": list(range(257, 288)),
    "C_up": list(range(288, 321)),
    "H_low": list(range(129, 145)),
    "H_up": list(range(145, 161)),
    "N_low": list(range(65, 73)),
    "N_up": list(range(73, 81)),
    "Ce": [5],
}

molecules = [molecule1, molecule2, molecule3, molecule4, molecule5]
