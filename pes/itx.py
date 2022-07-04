#!/usr/bin/env python3
"""Prodigy が出す itx ファイルでは

    WAVES/S/N=(600,701) 'Spectrum_17_1'

    など、 "Spectrum" の項目をWave名として割り当てる仕様になっている。
    しかし、一つの.sleファイルで一意性を有しているのは "Spectrum ID"
    なので、そちらを用いた方がよい。

bash
cat *itx > all.itx
gsed -i -e "/IGOR/d" all.itx
gsed -i -e "1i IGOR" all.itx

みたいなsedを後に行うと、igor で all.itx を読み込めば良いので便利
"""
from __future__ import annotations
import sys
import argparse


def tune(itx_file, angle_correction: float | None = None) -> str:
    """_summary_

    Parameters
    ----------
    itx_file : _type_
        _description_

    Returns
    -------
    str
        _description_
    """
    modified_itx_file = []
    for line in itx_file:
        if line.startswith("X //Spectrum ID"):
            id = int(line.split("=")[1])
        if "User Comment" in line:
            try:
                user_comment = line.split("=", maxsplit=1)[1].strip()
            except IndexError:
                user_comment = ""
        if line.startswith("X ///Excitation Energy"):
            excitation_energy = line.split("=", maxsplit=1)[1].strip()
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
            if angle_correction:
                ## 1.3088 が 2021/11/24の解析から求めた値
                setscalex: list[str] = line.split()
                new_scale_x_left = float(setscalex[3][:-1]) / args.angle_correction
                new_scale_x_right = float(setscalex[4][:-1]) / args.angle_correction
                note: str = (
                    r"""X Note /NOCR 'ID_{:03}' "\r\nangle_correction:{}" """.format(
                        id, args.angle_correction
                    )
                )
                command_part = " ".join(line.split()[:-1])
                line = (
                    note
                    + """\r\nX SetScale/I x, {}, {}, {} {} 'ID_{:03}'\r\n""".format(
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
        modified_itx_file.append(line.strip() + "\r\n")
    return "".join(modified_itx_file)
