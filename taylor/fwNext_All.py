#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--slots", type=str,default='0,1,2,3,4,5,6') 
parser.add_argument("--tio", type=str)
parser.add_argument('--fwslot', type=int, default=0,choices=[0,1,2])
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
    surfs = { 0: 0x8c,
            1: 0x95,
            2: 0x9f,
            3: 0x9a,
            4: 0x87,
            5: 0x85,
            6: 0x91}
elif args.tio == '2':
    tios = (2, 0x40)
    surfs = { 0: 0x89,
            1: 0x88,
            2: 0x9e,
            3: 0x8b,
            4: 0xa1,
            5: 0x98}
elif args.tio == '3':
    tios = (3, 0x48)
    surfs = { 0: 0x93,
            1: 0x9b,
            2: 0x86,
            3: 0x8e,
            4: 0x90,
            5: 0x92 }
elif args.tio == 't':
    tios = (0, 0x48)
    surfs = { 3: 0xa3,
            4: 0xa4 }


hsk = HskEthernet()
hsk.send(HskPacket(tios[1], 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()
for s in slotList:
    try: 
        val = surfs[s]
    except: 
        print(f'Slot argument {s} for TURFIO PORT#{args.tio} is incorrect!')
        sys.exit()
    hsk.send(HskPacket(val, 'eFwNext', data=f"/lib/firmware/{args.fwslot}"))
    pkt = hsk.receive()
    hsk.send(HskPacket(val, 'eRestart', data=[0])) 
    time.sleep(0.5)
    check = b'/lib/firmware/' + str(args.fwslot).encode()
    print(check)
    if pkt.data != check:
        print(f"Updating fw failed!") 

time.sleep(1)
print(f'Firmware loaded from /mnt/bitstreams/{args.fwslot}')
