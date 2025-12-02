#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import time


parser = argparse.ArgumentParser()

parser.add_argument("--tio", type=str)
parser.add_argument('--fwslot', type=int, default=0,choices=[0,1,2])
args = parser.parse_args()

if args.tio == '0':
    tios = (0, 0x58)
    surfs = [ (0, 0x97),
            (1, 0xa0),
            (2, 0x99),
            (3, 0x8d),
            (4, 0x9d),
            (5, 0x94),
            (6, 0x8a) ]
elif args.tio == '1':
    tios = (1, 0x50)
    surfs = [ (0, 0x8c),
            (1, 0x95),
            (2, 0x9f),
            (3, 0x9a),
            (4, 0x87),
            (5, 0x85), 
            (6, 0x91)]
elif args.tio == '2':
    tios = (2, 0x40)
    surfs = [ (0, 0x89),
            (1, 0x88),
            (2, 0x9e),
            (3, 0x8b),
            (4, 0xa1),
            (5, 0x98)]
elif args.tio == '3':
    tios = (3, 0x48)
    surfs = [ (0, 0x93),
            (1, 0x9b),
            (2, 0x86),
            (3, 0x8e),
            (4, 0x90),
            (5, 0x92) ]
elif args.tio == 'spare':
    tios = (0, 0x48)
    surfs = [ (3, 0x9c), 
            (6, 0xa3) ]


hsk = HskEthernet()
hsk.send(HskPacket(tios[1], 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()
for s in surfs:
    hsk.send(HskPacket(s[1], 'eFwNext', data=f"/lib/firmware/{args.fwslot}"))
    pkt = hsk.receive()
    hsk.send(HskPacket(s[1], 'eRestart', data=[0])) 
    print(pkt)
    time.sleep(1)
print(f'Firmware loaded from /mnt/bitstreams/{args.fwslot}')
