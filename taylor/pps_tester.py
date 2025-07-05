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

dev.trig.rundly = 3

for i in range(args.start,args.stop,20): 
    dev.trig.pps_offset = i 
    es.open()
    dev.trig.runcmd(dev.trig.RUNCMD_RESET)
    dev.trig.pps_trig_enable = 1 
    time.sleep(1)
    dev.trig.pps_trig_enable = 0
    trig_count = dev.trig.trigger_count
    j = 0 
    while trig_count > 0: 
        e = es.event_receive()
        f = open(f'{args.filename}off{i}_{j}.pkl', 'wb')
        pickle.dump(e,f)
        f.close()
        j += 1 
        trig_count -= 1
    es.close()
    dev.trig.runcmd(dev.trig.RUNCMD_STOP)
