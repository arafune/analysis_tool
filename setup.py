# -*- coding: utf-8 -*-

import sys
from distutils.core import setup

reqpkgs = ["numpy", "lxml"]
setup(
    name="analysis_tool",
    version="0.0.1",
    author="Ryuichi Arafune",
    maintainer="Ryuichi Arafune",
    maintainer_email="ryuichi.arafune@gmail.com",
    description="Python tools for analyzing experimental data (STM, LPES,,,)",
    py_moddules=["stm.qpi" "stm.rhksm4"],
    requires=reqpkgs,
    data_files=[
        ("etc", ["rmanalysis_tool.py"]),
    ],
)
