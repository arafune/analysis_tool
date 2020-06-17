"""HREELS Lens parameter"""

import argparse


class Entry:
    """Class for an entry."""

    def __init__(self):
        pass


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
