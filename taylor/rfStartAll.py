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
import argparse
from itertools import chain


parser = argparse.ArgumentParser()

parser.add_argument("--tio", type=int)
parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))


dev = PueoTURF(None, 'Ethernet')

dev.trig.offset = 36
print('Default trig offset is 36 clocks!')
tio = PueoTURFIO((dev, args.tio), 'TURFGTP')

for slot in slotList:
    surf = PueoSURF((tio, slot), 'TURFIO')
    surf.trig_clock_en = 1
    surf.levelone.write(0x2008, 0x00000)
    surf.levelone.write(0x200C, 0x80000000)

print('Okeedokee, clocks started, all beams unmasked!')
