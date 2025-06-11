#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle


parser = argparse.ArgumentParser()
parser.add_argument('--tio',
                    help='slot of the TURFIO for the surfs enable',
                    type=lambda x : int(x,0))


args = parser.parse_args()

if args.tio == '0':
    tios = (0, 0x58)
    surfs = [ (0, 0x97),
            (1, 0xa0),
            (2, 0x99),
            (3, 0x8d),
            (4, 0x9d),
            (5, 0x94),
            (6, 0x8a) ]
elif args.tio == '1':
    tios = (1, 0x50)
    surfs = [ (0, 0x8c),
            (1, 0x95),
            (2, 0x9f),
            (3, 0x9a),
            (4, 0x87),
            (5, 0x85), 
            (6, 0x9c)]
elif args.tio == '2':
    tios = (2, 0x40)
    surfs = [ (0, 0x89),
            (1, 0x88),
            (2, 0x9e),
            (3, 0x8b),
            (4, 0xa1),
            (5, 0x98)]
elif args.tio == '3':
    tios = (3, 0x48)
    surfs = [ (0, 0x93),
            (1, 0x9b),
            (2, 0x96),
            (3, 0x8e),
            (4, 0x90),
            (5, 0x92) ]
elif args.tio =='t':
    tios = (3, 0x48)
    surfs = [ (0, 0x93) ]


hsk = HskEthernet()
hsk.send(HskPacket(tios[1], 'eEnable', [0x40, 0x40]))


for s in surfs:
    hsk.send(HskPacket(s[1], 'eStartState', data=[19])) 
    hsk.receive()
    hsk.send(HskPacket(s[1], 'eStartState'))
    hsk.receive().pretty()