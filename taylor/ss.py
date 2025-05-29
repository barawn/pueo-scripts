#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('addr',
                    help='housekeeping address of SURF to get start state',
                    type=lambda x : int(x,0))
args = parser.parse_args()

hsk = HskEthernet()
hsk.send(HskPacket(args.addr, 'eStartState'))
pkt = hsk.receive()
print(f'SURF start state: response {pkt.pretty()}')



