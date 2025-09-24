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
parser.add_argument("--nbeams", type=int, default=2) 
parser.add_argument("--nsteps", type=int, default=6)
parser.add_argument("--stepsize", type=int, default=-1E8)
# parser.add_argument("--filename", default = "thresh_scan.csv")

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))


dev = PueoTURF(None, 'Ethernet')

tio = PueoTURFIO((dev, args.tio), 'TURFGTP')

surfs = {}
for slot in slotList: 
    surfs[slot] = PueoSURF((tio, slot), 'TURFIO')

for step_idx in range(args.nsteps):
    for slot in slotList:
        surf = surfs[slot]
        surf.levelone.write(0x1808, step_idx*int(args.stepsize))# Apply integration time 
        time.sleep(0.1)
        toggle = surf.levelone.read(0x1804)
        time.sleep(0.1)
        while(surf.levelone.read(0x1804) == toggle):
            time.sleep(0.1)
        print(f"Seconds: {(surf.levelone.read(0x1808)/(1.0E9)):4.4f}, Threshold: {surf.levelone.read(0x0800):6d}")
        for idx in range(args.nbeams):
            rate=surf.levelone.read(0x400+4*idx)
            trigger_rate = rate & 0x0000FFFF
            subthreshold_rate = (rate & 0xFFFF0000) >> 16
            print(f"Tio:{args.tio}, Slot:{slot}, Beam:{idx}, Scaler:{trigger_rate}, Subscaler:{subthreshold_rate}")
        print("\n")
    print("*******\n")
