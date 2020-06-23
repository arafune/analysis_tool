"""HREELS Lens parameter"""

import argparse
import datetime


filament = ["IK", "PsiK", "R"]
Alens = ["A1", "DeltaA1", "A2", "DeltaA2", "A3", "DeltaA3"]
PreMono = ["EVM", "UVM", "DeltaVM", "DVM", "DeltaDVM"]
Mono = ["UM", "DeltaM", "DM", "DeltaDM"]
Blens = ["B1", "DeltaB1", "B2", "B3", "B4", "DeltaB4"]
Ana = ["UA", "DeltaA", "DA", "DeltaDA"]
Clens = ["C1", "DeltaC1", "C2", "C3", "DeltaC3"]
Linked = ["UA", "DA", "B1" "B2", "B3", "B4", "UM", "DM", "HM", "EVM", "UVM", "DVM"]


class Entry:
    """Class for an entry."""

    def __init__(self):
        pass


def label_str(labeltext):
    """Return tuple of date & time, resolution, intensity from 'Label' string.
    "2/14/20 7:43:28 PM : +7.48 meV, 192.65 pA"


    Example
    ---------
    >>> label_str("2/14/20 7:43:28 PM : +7.48 meV, 192.65 pA")
        (datetime.datetime(2020, 2, 14, 19, 43, 28), 7.48, 192.65)
    """
    tmp = labeltext.strip().split()
    day_time = datetime.datetime.strptime(
        tmp[0] + " " + tmp[1] + " " + tmp[2], "%m/%d/%y %I:%M:%S %p"
    )
    res = float(tmp[4])
    intensity = float(tmp[6])
    return day_time, res, intensity


def _to_list(params, *show_values):
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
        for i in show_values:
            tmp.appeend(entry[i])
        output.append(tmp)
    return output


def _md_table(lst):
    """Output table format from list

    Parameters
    ------------
    lst: list
        input list (list of list)

    Returns
    ---------
    str
    """
    output = ""
    for i in lst:
        output += "|" + "|".join(i) + "|\n"
    return output


def load_els_lens_parameter(filename):
    container = []
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
                    value = int(line.strip().split("\t")[2])
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
