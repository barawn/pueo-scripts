#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import time 
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('addr', type = lambda x : int(x,0))
args = parser.parse_args()
addr = args.addr

hsk = HskEthernet()
hsk.send(HskPacket(0x48, 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()
print('This takes 5 seconds to run! Be patient!')
hsk.send(HskPacket(addr, 'eFwParams', data = b'\x01\x00\x00\x00\x78\x00'))
pkt = hsk.receive()
hsk.send(HskPacket(addr, 'eStartState', data=[19]))
pkt = hsk.receive()
time.sleep(5)
hsk.send(HskPacket(addr, 'eStartState'))
pkt = hsk.receive()
print(pkt.pretty())
