#!/usr/bin/env python3
import datetime
import random
from time import sleep

for i in range(100):
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    a1=random.random()
    a2=random.random()
    print("{}\t{}\t{}".format(now, a1, a2))
    sleep(1)
