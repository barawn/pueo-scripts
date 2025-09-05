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

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))

dev = PueoTURF(None, 'Ethernet')

tio = PueoTURFIO((dev, args.tio), 'TURFGTP')


for slot in slotList: 
    surf = PueoSURF((tio, slot), 'TURFIO')
    
    lowset = (0xFFFFF & (0))
    highset = (0xFFFFFFFF & (0))
    surf.levelone.write(0x2008,lowset)#0x00000
    surf.levelone.write(0x200c,highset)#0x80000000)
    print(f"Lower mask set to: {lowset:08X}")
    print(f"Lower mask read:   {surf.levelone.read(0x2008):08X}")
    print(f"Upper mask set to: {highset:08X}")
    print(f"Upper mask read:   {surf.levelone.read(0x200c):08X}")
    print(f'Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}')

    
    for mask_idx in range(32):        
        lowset = (0xFFFFF & (0x1<<mask_idx))
        highset = (0xFFFFFFFF & (0x1<<mask_idx))
        surf.levelone.write(0x2008,lowset)#0x00000
        surf.levelone.write(0x200c,highset)#0x80000000)
        print(f"Lower mask set to: {lowset:08X}")
        print(f"Lower mask read:   {surf.levelone.read(0x2008):08X}")
        print(f"Upper mask set to: {highset:08X}")
        print(f"Upper mask read:   {surf.levelone.read(0x200c):08X}")
        print(f'Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}')
