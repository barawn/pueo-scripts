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

dev.trig.mask = 201326591 # for just surf 26

es.open()
dev.trig.runcmd(dev.trig.RUNCMD_RESET)
time.sleep(15) 
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
