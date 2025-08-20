# calibration freeze bullshit
# YOU NEED pyrfdc IN YOUR PYTHONPATH
# YOU NEED THE libunivrfdc.so DIRECTORY IN YOUR LD_LIBRARY_PATH

import os
from pathlib import Path

from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from pyrfdc import PyRFDC

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--tio", type=int)
parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")
parser.add_argument('--disable',
                    action='store_true')

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))


dev = PueoTURF(None, 'Ethernet')

tio = PueoTURFIO((dev, args.tio), 'TURFGTP')

for slot in slotList: 
    surf = PueoSURF((tio, slot), 'TURFIO')
    if not args.disable:
        surf.cal_path_enable = 1
        print(f'Cal path enabled SURF slot {slot}')
    else: 
        surf.cal_path_enable = 0
        print(f'Cal path disabled SURF slot {slot}')


