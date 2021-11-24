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
    parser.add_argument("--angle_correction", type=float, metavar="Angle coefficient")
    parser.add_argument("itx_file")
    args = parser.parse_args()
    user_comment: str = ""
    id: int
    with open(args.itx_file) as itx_file:
        if args.output:
            output = open(args.output, "w")
        for line in itx_file:
            if line.startswith("X //Spectrum ID"):
                id = int(line.split("=")[1])
            if "User Comment" in line:
                try:
                    user_comment = line.split("=", maxsplit=1)[1].strip()
                except IndexError:
                    user_comment = ""
            if line.startswith("X //Kinetic Energy"):
                excitation_energy: str = line.split("=", maxsplit=1)[1].strip()
            if line.startswith("WAVES/S/N"):
                command_part: str = line.split(maxsplit=1)[0]
                line = command_part + " 'ID_" + str(id).zfill(3) + "'\r\n"
            if line.startswith("END") and user_comment:
                line = (
                    "END\r\n"
                    + "X Note /NOCR "
                    + "'ID_"
                    + str(id).zfill(3)
                    + "'"
                    + ' "'
                    + user_comment
                    + '"'
                    + "\r\n"
                )
                line += (
                    "X Note /NOCR " + "'ID_" + str(id).zfill(3) + "'" + ' "'
                    r"\r\nExcitation_energy:" + excitation_energy + '"' + "\r\n"
                )
            if line.startswith("X SetScale/I x"):
                if args.angle_correction:
                    ## 1.3088 が 2021/11/24の解析から求めた値
                    setscalex: list[str] = line.split()
                    new_scale_x_left = float(setscalex[3][:-1]) / args.angle_correction
                    new_scale_x_right = float(setscalex[4][:-1]) / args.angle_correction
                    note: str = (
                        """X Note /NOCR 'ID_{:03}' "angle_correction:{}"\r\n""".format(
                            id, args.angle_correction
                        )
                    )
                    command_part = " ".join(line.split()[:-1])
                    line = (
                        note
                        + """X SetScale/I x, {}, {}, {} {} 'ID_{:03}'\r\n""".format(
                            new_scale_x_left,
                            new_scale_x_right,
                            setscalex[5],
                            setscalex[6],
                            id,
                        )
                    )
                else:
                    command_part = " ".join(line.split()[:-1])
                    line = command_part + " 'ID_" + str(id).zfill(3) + "'\r\n"
            if line.startswith("X SetScale/I y") or line.startswith("X SetScale/I d"):
                command_part = " ".join(line.split()[:-1])
                line = command_part + " 'ID_" + str(id).zfill(3) + "'\r\n"
            if args.output:
                output.write(line.strip() + "\r\n")
            else:
                sys.stdout.write(line.strip() + "\r\n")
    if args.output:
        output.close()
