#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from EventTester import EventServer
import time


dev = PueoTURF()

dev.trig.offset = 37
tio1 = PueoTURFIO((dev, 0), 'TURFGTP')
surf1 = PueoSURF((tio1, 3), 'TURFIO')
surf2 = PueoSURF((tio1, 4), 'TURFIO')


surf1.trig_clock_en = 1
surf2.trig_clock_en = 1

surf1.levelone.write(0x1008, 0x00000)
surf1.levelone.write(0x100C, 0x80000000)
surf2.levelone.write(0x1008, 0x00000)
surf2.levelone.write(0x100C, 0x80000000)


print(f'Okeedokee, clocks started, offset {dev.trig.offset}, and all beams unmasked!')
