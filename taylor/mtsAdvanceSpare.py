#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import time 

hsk = HskEthernet()
hsk.send(HskPacket(0x48, 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()
print('This takes 5 seconds to run! Be patient!')
hsk.send(HskPacket(0xa3, 'eFwParams', data = b'\x01\x00\x00\x00\x78\x00'))
pkt = hsk.receive()
hsk.send(HskPacket(0x9c, 'eFwParams', data = b'\x01\x00\x00\x00\x78\x00'))
pkt = hsk.receive()
hsk.send(HskPacket(0xa3, 'eStartState', data=[19]))
pkt = hsk.receive()
hsk.send(HskPacket(0x9c, 'eStartState', data=[19]))
pkt = hsk.receive()
hsk.send(HskPacket(0xa3, 'eStartState', data=[19])) 
pkt = hsk.receive()
time.sleep(5)
hsk.send(HskPacket(0xa3, 'eStartState'))
pkt = hsk.receive()
print(pkt.pretty())
hsk.send(HskPacket(0x9c, 'eStartState'))
pkt = hsk.receive()
print(pkt.pretty())
