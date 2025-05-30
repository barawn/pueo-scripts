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
                    help='path to next software')

args = parser.parse_args()

n = None
if args.next:
    n = args.next
print(f'Next: {n}')
if args.local:
    hsk = HskSerial('/dev/hsklocal', srcId=0xFC)
else:
    hsk = HskEthernet()

# HskPacket autodetects str type and encodes it, so we can just pass
hsk.send(HskPacket(args.addr, 'eSoftNext', data=n))
pkt = hsk.receive()
print(f'SURF eSoftNext response: {pkt.pretty(asString=True)}')



