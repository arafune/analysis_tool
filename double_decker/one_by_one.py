#!/usr/bin/env python3
"""Module for analyzing the CePc2, TbPc2 on Au(111) vasp calculation
Code for vasp calculation results requested by Prof. Komeda (Nov, 2020)
(1x1) lattice
"""

from typing import Dict, List

DIFF_FROM_WHOLE_INDEX: Dict[str, int] = {
    "C": -1,
    "H": 63,
    "N": 95,
    "Ce": 111,
    "Au": 112,
}

molecule: Dict[str, List[int]] = {
    "C_low": list(range(32)),
    "C_up": list(range(32, 64)),
    "H_low": list(range(64, 80)),
    "H_up": list(range(80, 96)),
    "N_low": list(range(96, 104)),
    "N_up": list(range(104, 112)),
    "Ce": [112],
}

if __name__ == "__main__":
    pass