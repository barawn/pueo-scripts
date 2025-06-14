#!/usr/bin/env python3
import time

from PueoTURF import PueoTURF

# this is crap right now just turn on the ext pps

dev = PueoTURF()
dev.time.pps_holdoff = 100
dev.time.use_ext_pps = 1
time.sleep(1)
sec = dev.time.current_second
freq = (dev.time.last_pps - dev.time.llast_pps) & 0xFFFFFFFF
print(f'TURF time: {sec}')
print(f'Clock frequency: {freq}')
