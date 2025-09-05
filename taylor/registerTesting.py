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
import os


parser = argparse.ArgumentParser()

parser.add_argument("--tio", type=int)
parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")
parser.add_argument("--nbeams", type=int, default=2)
parser.add_argument("--verbose", "-v", action="store_true")
parser.add_argument("--testMasks", "-m", action="store_true")
parser.add_argument("--testThresholds", "-t", action="store_true")
parser.add_argument("--hideSURFExceptions", action="store_true")
parser.add_argument("--resetTrigGen", action="store_true")
parser.add_argument("--testThreshold", type=int, default=12345)

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))

dev = PueoTURF(None, 'Ethernet')

tio = PueoTURFIO((dev, args.tio), 'TURFGTP')


for slot in slotList:
    if(args.hideSURFExceptions):
        stdout_orig = sys.stdout
        sys.stdout = open(os.devnull, "w")
    surf = PueoSURF((tio, slot), 'TURFIO')
    if(args.hideSURFExceptions):
        sys.stdout = stdout_orig
    print(f"***** SLOT {slot} *****")
    if(args.testMasks):
        lowset = (0xFFFFF & (0))
        highset = (0xFFFFFFFF & (0))
        surf.levelone.write(0x2008,lowset)#0x00000
        surf.levelone.write(0x200c,highset)#0x80000000)
        for mask_idx in range(32):        
            lowset = (0x3FFFF & (0x1<<mask_idx))
            highset = (0x3FFFFFFF & (0x1<<mask_idx))
            surf.levelone.write(0x2008,lowset)#0x00000
            surf.levelone.write(0x200c,highset)#0x80000000)
            if(lowset != surf.levelone.read(0x2008) or highset != surf.levelone.read(0x200C) or args.verbose):
                print(f"MASK {highset:X} FAILED")
                print(f"\tLower mask set to: {lowset:08X}")
                print(f"\tLower mask read:   {surf.levelone.read(0x2008):08X}")
                print(f"\tUpper mask set to: {highset:08X}")
                print(f"\tUpper mask read:   {surf.levelone.read(0x200c):08X}")
                print(f'\tMasks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}')
    if(args.testThresholds):
        if(args.resetTrigGen):
            surf.levelone.write(0x2004, 0x100)# Reset trigger generator
            surf.levelone.write(0x2004, 0x000)# Reset trigger generator
            # print(f'Trigger Generator Reset on Slot {slot}') # 

        if(args.testThreshold>0):
            for i in range(args.nbeams): 
                #surf.levelone.write(0x1000, 2)# Pause servo (no servo in V2) 
                surf.levelone.write(0x800 + i*4, args.testThreshold) #
                #if not args.freeze: 
                #    surf.levelone.write(0x1000, 1)
        if(args.testThreshold>0):
            for i in range(args.nbeams): 
                #surf.levelone.write(0x1000, 2)# Pause servo (no servo in V2) 
                surf.levelone.write(0xA00 + i*4, args.testThreshold) #
                #if not args.freeze: 
                #    surf.levelone.write(0x1000, 1)
        surf.levelone.write(0x1800, 2)# Apply new thresholds 
        time.sleep(0.1)
        if(surf.levelone.read(0x1800)):
            print(f'Threshold update stuck')
        if(args.testThreshold>0):
            for i in range(args.nbeams): 
                readback = surf.levelone.read(0x800 + i*4)
                if(readback != args.testThreshold):
                    print(f"FAILED: Trigger threshold set to {args.testThreshold}, read back {readback}")
        if(args.testThreshold>0):
            for i in range(args.nbeams):
                readback = surf.levelone.read(0xA00 + i*4)
                if(readback != args.testThreshold):
                    print(f"FAILED: Trigger sub-threshold set to {args.testThreshold}, read back {readback}") 
                


        
