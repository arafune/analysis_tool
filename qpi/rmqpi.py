#! python
# -*- coding: utf-8 -*-
"""
Created on Nov. 25 (2016).

@author: Ryuichi Arafune
"""

if __name__ == '__main__':
    import sys
    import os
    logfile = sys.argv[1] if len(sys.argv) > 1 else 'install-qpi.txt'
    file = open(logfile)
    for line in file:
        line = line.rstrip('\n')
        try:
            os.remove(line)
        except FileNotFoundError:
            pass
        try:
            os.removedirs(os.path.dirname(line))
        except OSError:
            pass
