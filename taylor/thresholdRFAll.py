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

parser.add_argument("--tio", type=int)
parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")
parser.add_argument("--threshold", type=int)

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))


dev = PueoTURF(None, 'Ethernet')

tio = PueoTURFIO((dev, args.tio), 'TURFGTP')

for slot in slotList: 
    surf = PueoSURF((tio, slot), 'TURFIO')

    for i in range(49): 
        surf.levelone.write(0x1000, 2) 
        surf.levelone.write(0x0800 + i*4, args.threshold) 
        surf.levelone.write(0x1000, 1)

print(f'Yippee, threshold {args.threshold}')