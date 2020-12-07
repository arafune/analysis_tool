#!/usr/bin/env python3

"""Module for analyzing the CePc2 on monolayer CePc2 on Au(111) vasp calculation
Code for vasp calculation results requested by Prof. Komeda (Nov, 2020)

(2x2) 
"""

import itertools
from typing import Dict, List
from double_decker import two_by_two as two_by_two

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
    "C_low": list(range(257, 289)),
    "C_up": list(range(289, 321)),
    "H_low": list(range(129, 145)),
    "H_up": list(range(145, 161)),
    "N_low": list(range(65, 73)),
    "N_up": list(range(73, 81)),
    "Ce": [5],
}

molecules = [molecule1, molecule2, molecule3, molecule4, molecule5]


def test_check_independent_index() -> None:
    index_set = [
        set(two_by_two.series_index(mol, diff_from_series_index=DIFF_FROM_SERIES_INDEX))
        for mol in molecules
    ]
    for i in index_set:
        assert len(i) == 113
    for c in list(itertools.combinations([0, 1, 2, 3, 4], 2)):
        assert len(index_set[c[0]] & index_set[c[1]]) == 0


def test_check_the_number_of_atoms_mol() -> None:
    for mol in molecules:
        assert len(mol["C_up"]) == 32
        assert len(mol["C_low"]) == 32
        assert len(mol["H_up"]) == 16
        assert len(mol["H_low"]) == 16
        assert len(mol["N_up"]) == 8
        assert len(mol["N_low"]) == 8


if __name__ == "__main__":
    test_check_independent_index()