#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from EventTester import EventServer
import time

parser = argparse.ArgumentParser()
parser.add_argument('--stop', type=int) 
parser.add_argument('--start', type=int)
parser.add_argument('--filename')
args = parser.parse_args()

dev = PueoTURF()
es = EventServer()


for i in range(args.start,args.stop,5): 
    dev.trig.pps_offset = i 
    es.open()
    dev.trig.runcmd(dev.trig.RUNCMD_RESET)
    time.sleep(5)
    trig_count = dev.trig.trigger_count
    e = es.event_receive()
    f = open(f'{args.filename}off{i}_{j}.pkl', 'wb')
    pickle.dump(e,f)
    f.close()
    for i in range(449):
        es.es.recv(1032)
    es.close()
    dev.trig.runcmd(dev.trig.RUNCMD_STOP)
