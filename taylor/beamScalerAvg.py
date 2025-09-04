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

tio = PueoTURFIO((dev, 3), 'TURFGTP') 
surf = PueoSURF((tio, 5), 'TURFIO') 
# turfio 3 slots 5 and 6 
TFscalers = []
beamscalers = []
for i in range(120): 
    beamscalers.append(surf.levelone.read(0x400+4*5))
    TFscalers.append(dev.trig.scaler.read(29 * 4))
    time.sleep(1)

print(f'Average scaler SURF Slot 5: {sum(TFscalers) / len(TFscalers) }')
print(f'Average scaler beam 5: {sum(beamscalers) / len(beamscalers) }')
