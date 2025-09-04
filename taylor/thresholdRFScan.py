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
parser.add_argument("--min", type=int, default=50000)
parser.add_argument("--max", type=int, default=120000)
parser.add_argument("--step", type=int, default=1000)
parser.add_argument("--filename", default = "thresh_scan.csv")

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))


dev = PueoTURF(None, 'Ethernet')

tio = PueoTURFIO((dev, args.tio), 'TURFGTP')

surfs = {}
for slot in slotList: 
    surfs[slot] = PueoSURF((tio, slot), 'TURFIO')

with open(args.filename, "w") as outfile:
    outfile.write("tio, slot, beam, threshold, scaler, subscaler\n")
    for threshold_value in range(args.min, args.max, args.step):
        for slot in slotList:
            surf = surfs[slot]
            if(threshold_value>0):
                for idx in range(args.nbeams): 
                    #surf.levelone.write(0x1000, 2)# Pause servo (no servo in V2) 
                    surf.levelone.write(0x800 + idx*4, threshold_value) #
                    #if not args.freeze: 
                    #    surf.levelone.write(0x1000, 1)
            if(threshold_value>0):
                for idx in range(args.nbeams): 
                    #surf.levelone.write(0x1000, 2)# Pause servo (no servo in V2) 
                    surf.levelone.write(0xA00 + idx*4, threshold_value) #
                    #if not args.freeze: 
                    #    surf.levelone.write(0x1000, 1)
            surf.levelone.write(0x1800, 2)# Apply new thresholds 
            time.sleep(0.1)
            if(surf.levelone.read(0x1800)):
                raise Exception(f'Threshold update.... failed?')
            toggle = surf.levelone.read(0x1804)
            time.sleep(0.1)
            while(surf.levelone.read(0x1804) == toggle):
                time.sleep(0.1)
            for idx in range(args.nbeams):
                rate=surf.levelone.read(0x400+4*idx)
                trigger_rate = rate & 0x0000FFFF
                subthreshold_rate = (rate & 0xFFFF0000) >> 16
                outfile.write(f"{args.tio}, {slot}, {idx}, {threshold_value}, {trigger_rate}, {subthreshold_rate}\n")
        print(f"Scanned {threshold_value:d}")
        print(f"{args.tio}, {slot}, {idx}, {threshold_value}, {trigger_rate}, {subthreshold_rate}\n")
