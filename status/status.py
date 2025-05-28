#!/usr/bin/env python3

from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--surf",
                    help="also output the SURF status which will be VERY verbose")
args = parser.parse_args()

dev = PueoTURF(None, 'Ethernet')
dev.status()
tios = [ None, None, None, None ]
for i in range(4):
    try:
        tio = PueoTURFIO((dev, i), 'TURFGTP')
        tio.status()
        tios[i] = tio
    except Exception as e:
        print(f'Skipping TURFIO{i}: {repr(e)}')

if args.surf:
    for i in range(4):
        if tios[i] is not None:
            for j in range(7):
                try:
                    surf = PueoSURF((tios[i], j), 'TURFIO')
                    surf.status()
                except Exception as e:
                    print(f'Skipping SURF{j} on TURFIO{i}: {repr(e)}')
                    
                    
