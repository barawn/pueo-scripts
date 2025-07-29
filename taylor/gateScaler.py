#!/usr/bin/env python3

from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from pueo.common.term import Term

import time
import sys
import argparse
from itertools import chain


parser = argparse.ArgumentParser()

parser.add_argument("--tio", type=int)
parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")
parser.add_argument("--undo", action='store_true')

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))


dev = PueoTURF(None, 'Ethernet')

dev.trig.scaler.gate_sel = dev.trig.GpiSelect.TURFIO3

gate_en_val = 0
for slot in slotList: 
    if not args.undo:
        gate_en_val += 1 << (8 * args.tio + slot)
    else: 
        dev.trig.scaler.gate_en = 0 
dev.trig.scaler.gate_en = gate_en_val