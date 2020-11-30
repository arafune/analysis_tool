#!/usr/bin/env python3

"""Module for analyzing the CePc2 on monolayer CePc2 on Au(111) vasp calculation
Code for vasp calculation results requested by Prof. Komeda (Nov, 2020)

(2x2) 
"""

from typing import Dict, List

DIFF_FROM_WHOLE_INDEX: Dict[str, int] = {
    "C": -1,
    "H": 319,  # <- 255
    "N": 479,  # <- 383
    "Ce": 559,
    "Au": 564,
}


molecule5: Dict[str, List[int]] = {
    "C_low": list(range(257, 288)),
    "C_up": list(range(288, 321)),
    "H_low": list(range(129, 145)),
    "H_up": list(range(145, 161)),
    "N_low": list(range(65, 73)),
    "N_up": list(range(73, 81)),
    "Ce": [1],
}
