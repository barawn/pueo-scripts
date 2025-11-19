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
parser.add_argument("--unmaskall", action="store_true")
parser.add_argument("--maskall", action="store_true")
parser.add_argument("--setLowerMask", type=str, default=None)
parser.add_argument("--setUpperMask", type=str, default=None)

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))

dev = PueoTURF(None, 'Ethernet')

tio = PueoTURFIO((dev, args.tio), 'TURFGTP')


for slot in slotList: 
    surf = PueoSURF((tio, slot), 'TURFIO')


    if(not args.setUpperMask is None):
        surf.levelone.write(0x200c,int(args.setUpperMask,16))
        print(f'Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}')    
    if(not args.setLowerMask is None):
        surf.levelone.write(0x2008,int(args.setLowerMask,16))
        print(f'Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}')    
    
    if(args.unmaskall):
        surf.levelone.write(0x2008,0x00000000)
        surf.levelone.write(0x200c,0x80000000)
        print(f'Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}')
    elif(args.maskall):
        surf.levelone.write(0x2008,0x0003FFFF)
        surf.levelone.write(0x200c,0xFFFFFFFF)
        print(f'Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}')    
    

