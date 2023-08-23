"""HREELS Lens parameter"""


from __future__ import annotations

import argparse
import datetime
import itertools
from pathlib import Path
from typing import Iterable

filament: list[str] = ["IK", "PsiK", "R"]
Alens: list[str] = ["A1", "DeltaA1", "A2", "DeltaA2", "A3", "DeltaA3"]
PreMono: list[str] = ["EVM", "UVM", "DeltaVM", "DVM", "DeltaDVM"]
Mono: list[str] = ["UM", "DeltaM", "DM", "DeltaDM"]
Blens: list[str] = ["B1", "DeltaB1", "B2", "B3", "B4", "DeltaB4"]
Ana: list[str] = ["UA", "DeltaA", "DA", "DeltaDA"]
Clens: list[str] = ["C1", "DeltaC1", "C2", "C3", "DeltaC3"]
Linked: list[str] = [
    "UA",
    "DA",
    "B1",
    "B2",
    "B3",
    "B4",
    "UM",
    "DM",
    "HM",
    "EVM",
    "UVM",
    "DVM",
]


def label_str(
    labeltext: str,
) -> tuple[datetime.datetime, float, float] | tuple[None, None, None]:
    """Return tuple of date & time, resolution, intensity from 'Label' string.


    Parameters
    --------------
    labeltext: str
        String of "Label" item in ELS parameter data,
        such as "2/14/20 7:43:28 PM : +7.48 meV, 192.65 pA"

    Returns
    ----------
    tuple
        date&time, resolution, intensity


    Example
    ---------
    >>> label_str("2/14/20 7:43:28 PM : +7.48 meV, 192.65 pA")
        (datetime.datetime(2020, 2, 14, 19, 43, 28), 7.48, 192.65)
    """
    tmp = labeltext.strip()[1:-1].split()
    try:
        day_time = datetime.datetime.strptime(
            tmp[0] + " " + tmp[1] + " " + tmp[2], "%m/%d/%y %I:%M:%S %p"
        )
        return day_time, float(tmp[4]), float(tmp[6])
    except IndexError:
        return None, None, None


def _to_list(
    params: dict,
    *show_values: tuple,
    the_date: datetime.datetime = datetime.datetime(1970, 1, 1, 0, 0, 0),
) -> list:
    """Return List of the EELS parameter.

    Parameters
    -------------
    params: dict
        EELS lens parameter data

    show_values: tuple
        item names to store value.

    Returns
    ---------
        list
    """
    output = []
    for entry in params:
        tmp = []
        for i in itertools.chain.from_iterable(show_values):
            if i == "Date":
                try:
                    if entry[i] > the_date:
                        tmp.append(entry[i].strftime("%m/%d %H:%M:%S"))
                    else:
                        break
                except TypeError:
                    break
            else:
                tmp.append(entry[i])
        if tmp:
            output.append(tmp)
    return output


def _md_table(lst: Iterable) -> str:
    """Output table format from list

    Parameters
    ------------
    lst: list
        input list (list of list)

    Returns
    ---------
    str
        text output
    """
    output = ""
    for i in lst:
        output += "|" + "|".join(i) + "|\n"
    return output


def load_els_lens_parameter(filename: str | Path) -> list[dict[str, str | float]]:
    """Parse lens parameter file.

    Parameters
    -------------
    filename: str, pathlib.Path
        filename of EELS parameter

    Returns
    ----------
    list
        EELS parameter data
    """
    container = []
    an_entry: dict[str, str | float]
    with open(filename, "r") as f:
        for line in f:
            if "<D" in line[0:2]:
                an_entry = {}
                continue
            if "D>" in line[0:2]:
                container.append(an_entry)
                continue
            if "<EOF>" in line:
                break
            if "[" in line or "]" in line:
                continue
            else:
                try:
                    value: int | float | str = int(line.strip().split("\t")[2])
                except ValueError:
                    try:
                        value = float(line.strip().split("\t")[2])
                    except ValueError:
                        value = line.strip().split("\t")[2]
                an_entry[line.strip().split("\t")[1][1:-1]] = value
    return container


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="HREELS parameter analyzer",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    args = parser.parse_args()
    container = []
    for filename in args.prms:
        container.extend(load_els_lens_parameter(filename))
