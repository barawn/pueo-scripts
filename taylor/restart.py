#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('addr',
                    help='housekeeping address of SURF to restart',
                    type=lambda x : int(x,0))
args = parser.parse_args()

hsk = HskEthernet()
hsk.send(HskPacket(args.addr, 'eRestart', data=[0]))

