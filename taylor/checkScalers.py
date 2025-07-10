#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from EventTester import EventServer
import time

dev = PueoTURF()

print(dev.trig.scaler.scalers(verbose = True))