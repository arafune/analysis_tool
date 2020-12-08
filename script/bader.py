#!/usr/bin/env python3
"""bader analysis"""


import argparse
import bz2
from pathlib import Path
import subprocess
from typing import Union
import vaspy
from vaspy.chgcar import CHGCAR


def ref_chgcar(aeccar0: CHGCAR, aeccar2: CHGCAR) -> None:
    """Merge to chgcar"""
    if Path("CHGCAR_sum").exists():
        raise RuntimeError("CHGCAR_sum already exists")
    aeccar0.merge(aeccar2).save("CHGCAR_sum")


def run_bader(
    logfile_path: Union[Path, str],
    chgcar_path: Union[Path, str],
    chgcar_sum_path: Union[Path, str],
) -> None:
    if isinstance(chgcar_path, str):
        chgcar_path = Path(chgcar_path)
    if chgcar_path.suffix == ".bz2":
        uncompress_chgcar_path: str = chgcar_path.stem
        with bz2.open(chgcar_path, "rb") as bz2file:
            contents = bz2file.read()
            with open(uncompress_chgcar_path, "wb") as uncompress:
                uncompress.write(contents)
    else:
        uncompress_chgcar_path = chgcar_path.name

    if not Path(logfile_path).exists():
        with (open(logfile_path, "w")) as logfile:
            try:
                subprocess.run(
                    ["bader", uncompress_chgcar_path, "-ref", str(chgcar_sum_path)],
                    stdout=logfile,
                    stderr=subprocess.PIPE,
                    check=True,
                )
            except subprocess.CalledProcessError:
                print("Error in bader")


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--logfile", default="bader.log")
    parser.add_argument("aeccar0")
    parser.add_argument("aeccar2")
    parser.add_argument("chgcar")

    args = parser.parse_args()
    ref_chgcar(
        vaspy.load(args.aeccar0, mode="CHGCAR"), vaspy.load(args.aeccar2, mode="CHGCAR")
    )
    run_bader(
        logfile_path=args.logfile, chgcar_path=args.chgcar, chgcar_sum_path="CHGCAR_sum"
    )
