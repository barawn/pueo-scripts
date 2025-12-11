#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--tio", type=str, default="0,1,2,3", 
        help="comma-separated list of TURFIOs to initialize")
parser.add_argument("--slots", type=str)
parser.add_argument("--procOff", type=int)

args = parser.parse_args()
slotList=list(map(int,args.slots.split(',')))
if args.tio == '0':
    tios = (0, 0x58)
    surfs = {0: 0x97,
            1: 0xa0,
            2: 0x99,
            3: 0x8d,
            4: 0x9d,
            5: 0x94,
            6: 0x8a }
elif args.tio == '1':
    tios = (1, 0x50)
    surfs = {0: 0x8c,
            1: 0x95,
            2: 0x9f,
            3: 0x9a,
            4: 0x87,
            5: 0x85,
            6: 0x91}
elif args.tio == '2':
    tios = (2, 0x40)
    surfs = {0: 0x89,
            1: 0x88,
            2: 0x9e,
            3: 0x8b,
            4: 0xa1,
            5: 0x98}
elif args.tio == '3':
    tios = (3, 0x48)
    surfs = {0: 0x93,
            1: 0x9b,
            2: 0x86,
            3: 0x8e,
            4: 0x90,
            5: 0x92 }
elif args.tio == 'spare':
    tios = (0, 0x48)
    surfs = {3: 0x9c, 
            6: 0xa3}

    
hsk = HskEthernet()
hsk.send(HskPacket(tios[1], 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()
if args.procOff==1:
    for s in slotList:
        hsk.send(HskPacket(surfs[s], 'eSleep', data = [0x82]))
        pkt = hsk.receive()

    hsk.send(HskPacket(tios[1], 'eEnable', [0x40, 0x00])); pkt = hsk.receive()
    print(f'TURFIO PORT#{args.tio}: All SURF processors off!')
else:
    print(f'TURFIO PORT#{args.tio}: Processors off skipped!')
