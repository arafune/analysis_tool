#!/usr/bin/env python3
"""Prodigy が出す itx ファイルでは

    WAVES/S/N=(600,701) 'Spectrum_17_1'

    など、 "Spectrum" の項目をWave名として割り当てる仕様になっている。
    しかし、一つの.sleファイルで一意性を有しているのは "Spectrum ID"
    なので、そちらを用いた方がよい。
"""

import sys
import argparse

if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        metavar="file_name",
        help="""output file name.
if not specified, use standard output""",
    )
    parser.add_argument("itx_file")
    args = parser.parse_args()
    id: int
    with open(args.itx_file) as itx_file:
        if args.output:
            output = open(args.output, "w")
        for line in itx_file:
            if "//Spectrum ID" in line:
                id = int(line.split("=")[1])
            if line.startswith("WAVES/S/N"):
                command_part: str = line.split(maxsplit=1)[0]
                line = command_part + " 'ID_" + str(id).zfill(3) + "'\r\n"
            if line.startswith("X SetScale"):
                command_part = " ".join(line.split()[:-1])
                line = command_part + " 'ID_" + str(id).zfill(3) + "'\r\n"
            if args.output:
                output.write(line.strip() + "\r\n")
            else:
                sys.stdout.write(line.strip() + "\r\n")
    if args.output:
        output.close()
