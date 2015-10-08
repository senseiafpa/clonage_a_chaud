#!/usr/bin/env python2.7

import random
import time
import sys

while True:
    r = random.sample([1, 2, 3, 4], 1)[0]
    sys.stdout.write("%i"%r)
    sys.stdout.flush()
    time.sleep(r)
    msg = sys.stdin.read(10)
    sys.stdout.write("a")
    sys.stdout.flush()
