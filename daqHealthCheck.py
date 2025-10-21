#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from EventTester import EventServer
import time



"""tio0 = (0, 0x58)
surf0 = [ (0, 0x97),
        (1, 0xa0),
        (2, 0x99),
        (3, 0x8d),
        (4, 0x9d),
        (5, 0x94),
        (6, 0x8a) ]

tio1 = (1, 0x50)
surf1 = [ (0, 0x8c),
        (1, 0x95),
        (2, 0x9f),
        (3, 0x9a),
        (4, 0x87),
        (5, 0x85), 
        (6, 0x91)]

tio2 = (2, 0x40)
surf2 = [ (0, 0x89),
        (1, 0x88),
        (2, 0x9e),
        (3, 0x8b),
        (4, 0xa1),
        (5, 0x98)]

tio3 = (3, 0x48)
surf3 = [ (0, 0x93),
        (1, 0x9b),
        (2, 0x86),
        (3, 0x8e),
        (4, 0x90),
        (5, 0x92) ]

tios = [tio0, tio1, tio2, tio3]
surfs = [surf0, surf1, surf2, surf3]"""

tio3 = (0, 0x48)
surf3 = [ (3, 0x9c),
        (6, 0xa3) ]

tios = [ tio3 ]
surfs = [ surf3 ]
dev = PueoTURF()
lol = 0
for i in range(4): 
    try: 
        tio = PueoTURFIO((dev, i), 'TURFGTP') 
    except: 
        if i ==1: 
            for j in range(7,14): 
                lol |= ( 1 << j) 
        elif i ==2: 
            for j in range(14,21): 
                lol |= ( 1 << j)
        elif i ==3: 
            for j in range(21,28): 
                lol |= ( 1 << j)  
    if i == 0 or i == 1: 
        for j in range(7): 
            surf = PueoSURF((tio, j), 'TURFIO')
            lol |= ( surf.lol << j) 
    else: 
        for k in range(7): 
            surf = PueoSURF((tio, k), 'TURFIO')
            lol |= ( surf.lol << k) 
"""
for i in range(4): 
    tio = PueoTURFIO((dev, i), 'TURFGTP') 
    if i == 0 or i == 1: 
        for j in range(7): 
            surf = PueoSURF((tio, j), 'TURFIO')
            lol |= ( surf.lol << j) 
    else: 
        for k in range(): 
            surf = PueoSURF((tio, k), 'TURFIO')
            lol |= ( surf.lol << k) 
"""