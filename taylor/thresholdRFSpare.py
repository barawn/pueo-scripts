#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from EventTester import EventServer
import time

parser = argparse.ArgumentParser()
parser.add_argument('--threshold', type=int)
args = parser.parse_args()


dev = PueoTURF()
es = EventServer()

tio1 = PueoTURFIO((dev, 0), 'TURFGTP')

surf1 = PueoSURF((tio1, 5), 'TURFIO')

for i in range(49): 
    surf1.levelone.write(0x1000, 2) 
    surf1.levelone.write(0x0800 + i*4, args.threshold) 
    surf1.levelone.write(0x1000, 1)
print(f'Yippee, threshold {args.threshold}')
print(surf1.levelone.read(0x0800))

