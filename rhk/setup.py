# -*- coding: utf-8 -*-

from distutils.core import setup
import sys

reqpkgs = ['numpy']
setup(name='rhk',
        version='0.0.1',
        author='Ryuichi Arafune',
        maintainer='Ryuichi Arafune',
        maintainer_email='ryuichi.arafune@gmail.com',
        description='RHK sm4 file loader',
        py_moddules=[
            'rhk.rhksm4'
            ],
        requires=reqpkgs,
        data_files=[('etc', ['rmrhk.py']),]
        )

