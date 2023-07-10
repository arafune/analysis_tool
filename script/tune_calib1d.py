#! /usr/bin/env python3

"""Script for tuning calib1d.

Calib1D contains the calibration of PHOIBOS energy analyser.

このキャリブレーションデータは 場所ーエネルギーシフトについて一次関数になっていると思
って良い (はず)、だが何らかの都合で1次関数から微妙にずれるときがある(Calib1Dを作るた
めに用いる Spectraの数が少ないときに起きる?)。これを1次関数でフィットし直す。.
"""

import argparse
from logging import INFO, Formatter, StreamHandler, getLogger

from pes.calib1d import Calib1d

LOGLEVEL = INFO
logger = getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
formatter = Formatter(fmt)
handler = StreamHandler()
handler.setLevel(LOGLEVEL)
logger.setLevel(LOGLEVEL)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("calib_file", help="""calib1d file""")
args = parser.parse_args()

stem, suffix = args.calib_file.rsplit(".", 1)
calib1d = Calib1d(args.calib_file)

calib1d.comment("Linearized by RA.")
calib1d.linearlization()
calib1d.save(stem + "_fix." + suffix)
