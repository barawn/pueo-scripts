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
parser.add_argument("--threshold", type=int, default=-1)
parser.add_argument("--subthreshold", type=int, default=-1)
parser.add_argument("--unmask", action="store_true")#untested

#parser.add_argument("--freeze", action='store_true') # No servo in V2

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))


dev = PueoTURF(None, 'Ethernet')

tio = PueoTURFIO((dev, args.tio), 'TURFGTP')


for slot in slotList: 
    surf = PueoSURF((tio, slot), 'TURFIO')
    surf.levelone.write(0x2004, 0x100)# Reset trigger generator
    surf.levelone.write(0x2004, 0x000)# Reset trigger generator
    print(f'Trigger Generator Reset on Slot {slot}')

    if(args.threshold>0):
        for i in range(49): 
            #surf.levelone.write(0x1000, 2)# Pause servo (no servo in V2) 
            surf.levelone.write(0x800 + i*4, args.threshold) #
            #if not args.freeze: 
            #    surf.levelone.write(0x1000, 1)
    if(args.subthreshold>0):
        for i in range(49): 
            #surf.levelone.write(0x1000, 2)# Pause servo (no servo in V2) 
            surf.levelone.write(0xA00 + i*4, args.subthreshold) #
            #if not args.freeze: 
            #    surf.levelone.write(0x1000, 1)
    surf.levelone.write(0x1800, 2)# Apply new thresholds 
    time.sleep(0.1)
    if(not surf.levelone.read(0x1800)):
        print(f'Threshold update success')
    else:
        print(f'Threshold update.... failed?')
    
    if(args.unmask):
        surf.levelone.write(0x2008,0x00000)
        surf.levelone.write(0x200c,0x80000000)
        print(f'Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}')
        
if(args.threshold > 0 and args.subthreshold > 0):
    print(f'Yippee, threshold {args.threshold} and subthreshold {args.subthreshold}')
elif(args.threshold > 0):
    print(f'Yippee, threshold {args.threshold}')
elif(args.subthreshold > 0):
    print(f'Yippee, subthreshold {args.subthreshold}')

