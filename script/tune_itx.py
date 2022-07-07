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
from pes.itx import tune

from logging import DEBUG, INFO, Formatter, StreamHandler, getLogger

LOGLEVEL = DEBUG
logger = getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
formatter = Formatter(fmt)
handler = StreamHandler()
handler.setLevel(LOGLEVEL)
logger.setLevel(LOGLEVEL)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        metavar="file_name",
        help="""output file name.
if not specified, use standard output""",
    )
    parser.add_argument(
        "--angle_correction",
        type=float,
        metavar="Angle coefficient",
        help="Angle correction coefficient (Usually not needed). Note that this is *not* offset.",
    )
    parser.add_argument(
        "itx_files", metavar="itx_file", nargs="+", help="itx file to be handled"
    )
    args = parser.parse_args()
    logger.debug(args)
    corrected_itx: list[str] = []
    for itx_file in args.itx_files:
        logger.info("itx_file name:{}".format(itx_file))
        with open(itx_file, "r") as itx:
            corrected_itx += tune(itx)
    corrected_itx = ["IGOR\r\n"] + [i for i in corrected_itx if i != "IGOR\r\n"]
    if args.output:
        with open(args.output, "w") as output_file:
            output_file.write("".join(corrected_itx))
    else:
        print("".join(corrected_itx))
