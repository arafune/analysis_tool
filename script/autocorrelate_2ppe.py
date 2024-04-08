#!/usr/bin/env python3
"""Plot auto correlator data"""

from __future__ import annotations

import argparse
from logging import INFO, Formatter, StreamHandler, getLogger
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np

from pes.prodigy_util import ProdigyItx

if TYPE_CHECKING:
    from matplotlib.figure import FigureBase

LOGLEVEL = INFO
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
        help="""output file name. if not specified, use standard output""",
    )
    parser.add_argument(
        "itx_files",
        metavar="itx_file",
        nargs="+",
        help="itx file to be analyzed",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        default=False,
        help="Build a Graph by using matplotlib",
    )
    args = parser.parse_args()
    logger.debug(args)
    positions: list[float] = []
    integrated_intensities: list[float] = []
    autocorrelation = []
    for itx_file in args.itx_files:
        logger.debug(f"itx_file name:{itx_file}")
        prodigy_itx = ProdigyItx(itx_file)
        integrated_intensity = prodigy_itx.integrated_intensity
        comment_string = str(prodigy_itx.params["User Comment"])
        comments = {}
        for i in comment_string.split(";"):
            try:
                item, value = i.split(":")
                comments[item] = value
                logger.debug(f"item:{item}, value:{value}")
            except ValueError:
                logger.debug(f"i is {i}. Its not item-value type data.")
        position = float(comments["Position"].split()[0])
        logger.debug(f"Position is: {position}")
        autocorrelation.append((position, integrated_intensity))
    if args.output:
        np.savetxt(args.output, np.array(autocorrelation), delimiter="\t")
    else:
        print(np.array(autocorrelation))
    if args.plot:
        fig: FigureBase = plt.figure(figsize=(8, 5))
        axs = fig.add_subplot(111)
        axs.scatter(np.array(autocorrelation).T[0], np.array(autocorrelation).T[1])
        axs.set_xlabel("Delayline position  ( mm )")
        axs.set_ylabel("Integrated intensity")
        if args.output:
            fig.savefig(args.output + ".png", dpi=300)
        else:
            fig.savefig("output.png", dpi=300)
