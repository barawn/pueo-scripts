#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from EventTester import EventServer
import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--stop', type=int) 
parser.add_argument('--filename')
parser.add_argument('--threshold')
args = parser.parse_args()


dev = PueoTURF()
es = EventServer()

tio1 = PueoTURFIO((dev, 0), 'TURFGTP')
tio2 = PueoTURFIO((dev, 3), 'TURFGTP')

surf1 = PueoSURF((tio1, 5), 'TURFIO')
surf2 = PueoSURF((tio2, 5), 'TURFIO')

if surf1.trig_clock_en != 1 or surf2.trig_clock_en != 1: 
    print("Yo, the RF stuff ain't set up right")
    sys.exit(1)

surf1.levelone.write(0x1008, 0x30000)
surf1.levelone.write(0x100C, 0xffffffff)
surf2.levelone.write(0x1008, 0x30000)
surf2.levelone.write(0x100C, 0xffffffff)

dev.trig.mask = 201326559

es.open()
dev.trig.runcmd(dev.trig.RUNCMD_RESET)

for i in range(args.stop): 
    e = es.event_receive()
    f = open(f'{args.filename}_{i}.pkl', 'wb')
    pickle.dump(e,f)
    f.close()

for i in range(449):
    es.es.recv(1032)

es.close()
dev.trig.runcmd(dev.trig.RUNCMD_STOP)
