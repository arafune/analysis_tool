#!/usr/bin/env python3
"""Prodigy が出す itx ファイルでは

    WAVES/S/N=(600,701) 'Spectrum_17_1'

    など、 "Spectrum" の項目をWave名として割り当てる仕様になっている。
    しかし、一つの.sleファイルで一意性を有しているのは "Spectrum ID"
    なので、そちらを用いた方がよい。

"""
from __future__ import annotations

import argparse
from logging import DEBUG, Formatter, StreamHandler, getLogger

from pes.itx import tune

LOGLEVEL = DEBUG
logger = getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
formatter = Formatter(fmt)
handler = StreamHandler()
handler.setLevel(LOGLEVEL)
logger.setLevel(LOGLEVEL)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = True


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
        with open(args.output, "wb") as output_file:
            output_file.write(("".join(corrected_itx)).encode(encoding="utf-8"))
    else:
        print("".join(corrected_itx))
