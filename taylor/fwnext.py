#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--local',
                    help='use /dev/hsklocal instead of HskEthernet',
                    action='store_true')
parser.add_argument('addr',
                    help='housekeeping address of SURF to get start state',
                    type=lambda x : int(x,0))
parser.add_argument('--next',
                    type=str,
                    help='path to next firmware')

args = parser.parse_args()

if args.local:
    hsk = HskSerial('/dev/hsklocal', srcId=0xFC)
else:
    hsk = HskEthernet()
    
hsk.send(HskPacket(args.addr, 'eFwNext', data=args.nextfw.encode()))
pkt = hsk.receive()
print(f'SURF eFwNext response: {pkt.pretty(asString=True)}')



