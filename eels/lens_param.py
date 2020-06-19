"""HREELS Lens parameter"""

import argparse
import datetime


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
    parser.add_argument(
        "prms", nargs="+", metavar="EELS_lens_parameter_file(s)", type=str
    )

    args = parser.parse_args()
    container = []
    for filename in args.prms:
        container.extend(load_els_lens_parameter(filename))

    print(container)
