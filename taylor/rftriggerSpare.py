#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from EventTester import EventServer
import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--stop', type=int) 
parser.add_argument('--filename')
args = parser.parse_args()


dev = PueoTURF()
es = EventServer()

tio1 = PueoTURFIO((dev, 0), 'TURFGTP')

surf1 = PueoSURF((tio1, 6), 'TURFIO')

if surf1.trig_clock_en != 1 : 
    print("Yo, the RF stuff ain't set up right")
    sys.exit(1) 

dev.event.mask = 0b1110
dev.trig.mask = 536870847

es.open()
dev.trig.runcmd(dev.trig.RUNCMD_RESET)
dev.evstatus()

for i in range(args.stop): 
    e = es.event_receive()
    f = open(f'{args.filename}_{i}.pkl', 'wb')
    pickle.dump(e,f)
    f.close()

for i in range(449):
    es.es.recv(1032)

es.close()
dev.trig.runcmd(dev.trig.RUNCMD_STOP)
dev.evstatus()
