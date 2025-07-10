#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import time 


tio1 = (0, 0x58)
surf1 = [(5, 0x94)]


tio2 = (3, 0x48)
surf2 = [ (5, 0x92) ]



hsk = HskEthernet()
hsk.send(HskPacket(tio2[1], 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()
hsk.send(HskPacket(tio1[1], 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()
print('This takes 5 seconds to run! Be patient!')

hsk.send(HskPacket(surf1[1], 'eFwParams', data = b'\x01\x00\x00\x00\x78\x00'))
pkt = hsk.receive()
hsk.send(HskPacket(surf1[1], 'eStartState', data=[19])) 
pkt = hsk.receive()
hsk.send(HskPacket(surf2[1], 'eFwParams', data = b'\x01\x00\x00\x00\x78\x00'))
pkt = hsk.receive()
hsk.send(HskPacket(surf2[1], 'eStartState', data=[19])) 
pkt = hsk.receive()
time.sleep(5)

hsk.send(HskPacket(surf1[1], 'eStartState'))
pkt = hsk.receive()
print(pkt.pretty())
hsk.send(HskPacket(surf2[1], 'eStartState'))
pkt = hsk.receive()
print(pkt.pretty())
