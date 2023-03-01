#!/usr/bin/env python3
"""Generate POSCAR file from Wyckoff paramter

WTe2 only
"""
from __future__ import annotations

import json
from pathlib import Path


def load_wyckoff(filename: str | Path) -> dict[str, list[list[float]]]:
    with open(filename, "r") as json_file:
        return json.load(json_file)


def coordinate(wykcoff_position: list[float]) -> list[list[float]]:
    """Return direct coordinate"""
    direct_position = [
        wykcoff_position,
        [0.5, -wykcoff_position[1], wykcoff_position[2] + 0.5],
    ]
    return direct_position


if __name__ == "__main__":
    wte2 = load_wyckoff("Wte2_Wyckoff.json")
    print(wte2)
    lattice = (wte2[lattice][0], wte2[lattice][1], wte2[lattice][2])
    # (0, y, z )
    # (0.5, -y, 0.5+z)
