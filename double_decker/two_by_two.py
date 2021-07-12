#!/usr/bin/env python3
"""Module for analyzing the CePc2, TbPc2 on Au(111) vasp calculation
Code for vasp calculation results requested by Prof. Komeda (Nov, 2020)

(2x2) lattice
"""

import itertools

DIFF_FROM_SERIES_INDEX: dict[str, int] = {
    "C": -1,
    "H": 255,
    "N": 383,
    "Ce": 447,
    "Tb": 447,
    "Au": 451,
}


molecule1: dict[str, list[int]] = {
    "C_up": [
        136,
        227,
        140,
        144,
        152,
        243,
        156,
        160,
        231,
        161,
        235,
        239,
        247,
        177,
        251,
        255,
        165,
        194,
        169,
        173,
        181,
        210,
        185,
        189,
        132,
        198,
        206,
        202,
        148,
        214,
        222,
        218,
    ],
    "C_low": [
        104,
        112,
        108,
        36,
        120,
        52,
        124,
        128,
        39,
        67,
        43,
        47,
        55,
        83,
        59,
        63,
        69,
        1,
        73,
        77,
        85,
        17,
        89,
        93,
        6,
        98,
        10,
        14,
        22,
        114,
        26,
        30,
    ],
    "H_up": [72, 115, 80, 76, 81, 119, 123, 127, 85, 98, 89, 93, 102, 68, 106, 110],
    "H_low": [20, 56, 60, 64, 23, 35, 31, 27, 6, 10, 14, 50, 1, 37, 45, 41],
    "N_up": [41, 50, 36, 59, 63, 45, 54, 40],
    "N_low": [2, 17, 11, 28, 5, 23, 16, 30],
    "Ce": [1],
}


molecule2: dict[str, list[int]] = {
    "C_up": [
        135,
        228,
        139,
        143,
        151,
        244,
        155,
        159,
        232,
        162,
        236,
        240,
        248,
        178,
        252,
        256,
        166,
        193,
        170,
        174,
        182,
        209,
        186,
        190,
        131,
        197,
        201,
        205,
        147,
        213,
        217,
        221,
    ],
    "C_low": [
        107,
        111,
        51,
        119,
        123,
        127,
        35,
        103,
        44,
        48,
        56,
        84,
        60,
        64,
        40,
        68,
        74,
        78,
        86,
        18,
        90,
        94,
        2,
        70,
        9,
        13,
        113,
        21,
        25,
        29,
        5,
        97,
    ],
    "H_up": [71, 116, 75, 79, 82, 120, 124, 128, 86, 97, 90, 94, 67, 101, 105, 109],
    "H_low": [55, 19, 59, 63, 24, 36, 28, 32, 2, 38, 42, 46, 5, 49, 9, 13],
    "N_up": [42, 35, 60, 49, 53, 46, 64, 39],
    "N_low": [1, 18, 12, 27, 15, 29, 24, 6],
    "Ce": [2],
}

molecule3: dict[str, list[int]] = {
    "C_up": [
        134,
        225,
        138,
        142,
        150,
        241,
        154,
        158,
        163,
        229,
        237,
        233,
        179,
        245,
        253,
        249,
        196,
        167,
        175,
        171,
        183,
        212,
        187,
        191,
        130,
        200,
        204,
        208,
        146,
        216,
        224,
        220,
    ],
    "C_low": [
        106,
        110,
        50,
        118,
        122,
        126,
        34,
        102,
        41,
        45,
        53,
        81,
        57,
        61,
        37,
        65,
        75,
        79,
        19,
        87,
        91,
        95,
        3,
        71,
        12,
        16,
        24,
        116,
        28,
        32,
        8,
        100,
    ],
    "H_up": [70, 113, 74, 78, 83, 117, 121, 125, 91, 95, 87, 100, 66, 104, 108, 112],
    "H_low": [18, 54, 58, 62, 21, 33, 25, 29, 3, 39, 43, 47, 8, 12, 16, 52],
    "N_up": [43, 57, 34, 52, 47, 56, 61, 38],
    "N_low": [4, 19, 9, 26, 14, 21, 7, 32],
    "Ce": [3],
}


molecule4: dict[str, list[int]] = {
    "C_up": [
        133,
        137,
        141,
        226,
        242,
        157,
        153,
        149,
        230,
        164,
        234,
        238,
        246,
        180,
        250,
        254,
        129,
        199,
        207,
        203,
        145,
        215,
        223,
        219,
        168,
        195,
        172,
        176,
        184,
        211,
        188,
        192,
    ],
    "C_low": [
        105,
        109,
        101,
        33,
        117,
        121,
        125,
        49,
        38,
        66,
        42,
        46,
        54,
        58,
        62,
        82,
        4,
        72,
        76,
        80,
        88,
        92,
        96,
        20,
        7,
        99,
        11,
        15,
        23,
        115,
        27,
        31,
    ],
    "H_up": [69, 114, 73, 77, 84, 118, 122, 126, 88, 99, 92, 96, 65, 103, 107, 111],
    "H_low": [53, 17, 57, 61, 22, 34, 26, 30, 4, 40, 44, 48, 7, 51, 11, 15],
    "N_up": [44, 58, 33, 51, 48, 55, 37, 62],
    "N_low": [3, 20, 10, 25, 13, 22, 8, 31],
    "Ce": [4],
}

molecules: list[dict[str, list[int]]] = [molecule1, molecule2, molecule3, molecule4]
site_names: list[str] = ["C", "H", "N"]
positions: list[str] = ["up", "low"]


def series_index(
    molecule: dict[str, list[int]],
    diff_from_series_index: dict[str, int] = DIFF_FROM_SERIES_INDEX,
) -> list[int]:
    """Return series index (begin with "0") of molecule"""
    series = []
    for site, index in molecule.items():
        if site.startswith("C_"):
            series.extend([i + diff_from_series_index["C"] for i in index])
        elif site.startswith("N_"):
            series.extend([i + diff_from_series_index["N"] for i in index])
        elif site.startswith("H_"):
            series.extend([i + diff_from_series_index["H"] for i in index])
        elif site.startswith("Ce"):
            series.extend([i + diff_from_series_index["Ce"] for i in index])
        elif site.startswith("Tb"):
            series.extend([i + diff_from_series_index["Tb"] for i in index])
    return series


def test_check_independent_index() -> None:
    index_set = [set(series_index(mol)) for mol in molecules]
    for i in index_set:
        assert len(i) == 113
    for c in list(itertools.combinations([0, 1, 2, 3], 2)):
        assert len(index_set[c[0]] & index_set[c[1]]) == 0


def test_check_the_number_of_atoms_mol() -> None:
    for mol in molecules:
        assert len(mol["C_up"]) == 32
        assert len(mol["C_low"]) == 32
        assert len(mol["H_up"]) == 16
        assert len(mol["H_low"]) == 16
        assert len(mol["N_up"]) == 8
        assert len(mol["N_low"]) == 8


def test_check_not_overlapping() -> None:
    for mol in molecules:
        for site in site_names:
            for position in positions:
                assert len(set(sorted(mol[site + "_" + position]))) == len(
                    sorted(mol[site + "_" + position])
                )


if __name__ == "__main__":
    test_check_the_number_of_atoms_mol()
    test_check_not_overlapping()
    test_check_independent_index()
