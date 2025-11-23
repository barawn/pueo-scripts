#! /usr/bin/env python3

import time
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF


def registerWORK(surf, tio): 
    dev = PueoTURF()
    tio = PueoTURFIO((dev, tio), 'TURFGTP')
    try:
        surf = PueoSURF((tio, surf), 'TURFIO')
        print("SURF's there... why are you complaining?") 
    except:
        print('Well that sucks')

