#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from EventTester import EventServer
import time


dev = PueoTURF(None, 'Ethernet')

# turfio 3 slots 5 and 6 
slot5 = []
slot6 = []
for i in range(0, 5):#60): 
    slot5.append(dev.trig.scaler.read(28 * 4))
    slot6.append(dev.trig.scaler.read(29 * 4))
    time.sleep(1)
print(slot5)
print(slot6)
print(f'Average scaler SURF Slot 4: {sum(slot5) / len(slot5) }')
print(f'Average scaler SURF Slot 5: {sum(slot6) / len(slot6) }')
