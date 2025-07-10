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

tio1 = PueoTURFIO((dev, 0), 'TURFGTP')
tio2 = PueoTURFIO((dev, 3), 'TURFGTP')

surf1 = PueoSURF((tio1, 5), 'TURFIO')
surf2 = PueoSURF((tio2, 5), 'TURFIO')

print(f'SURF 5 Threshold: {surf1.levelone.read(0x0800)}')
print(f'SURF 26 Threshold: {surf2.levelone.read(0x0800)}')
print(dev.trig.scaler.scalers(verbose = True))
