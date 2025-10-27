#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from EventTester import EventServer

parser = argparse.ArgumentParser()
parser.add_argument('--stop', type=int) 
parser.add_argument('--mask', type=int, default=0) 
parser.add_argument('--filename')
args = parser.parse_args()

dev = PueoTURF()
es = EventServer()

from startup.eventStartup import eventStartup

eventStartup((dev, es), args.mask)
for i in range(0,(args.stop)): 
    dev.trig.soft_trig()
    e = es.event_receive()
    f = open(args.filename+'{}.pkl'.format(i), 'wb')
    pickle.dump(e,f)
    f.close()

es.close()
dev.trig.runcmd(dev.trig.RUNCMD_STOP)
print('Done!') 
