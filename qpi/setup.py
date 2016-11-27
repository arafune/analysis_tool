# -*- coding: utf-8 -*-

from distutils.core import setup
import sys

reqpkgs = ['numpy', 'matplotlib']
setup(name='qpi',
        version='0.0.1',
        author='Ryuichi Arafune',
        maintainer='Ryuichi Arafune',
        maintainer_email='ryuichi.arafune@gmail.com',
        description='QPI pattern analysis module'
        py_moddules=[
            'qpi.qpi'
            ],
        requires=reqpkgs,
        data_files=[('etc', ['rmqpi.py']),]
        )

