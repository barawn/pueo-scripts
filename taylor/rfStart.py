#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from EventTester import EventServer
import time


dev = PueoTURF()
es = EventServer()

dev.trig.offset = 27

tio1 = PueoTURFIO((dev, 0), 'TURFGTP')
tio2 = PueoTURFIO((dev, 3), 'TURFGTP')

surf1 = PueoSURF((tio1, 5), 'TURFIO')
surf2 = PueoSURF((tio2, 5), 'TURFIO')

surf1.trig_clock_en = 1
surf2.trig_clock_en = 1

print('Okeedokee, clocks started, offset 27!')