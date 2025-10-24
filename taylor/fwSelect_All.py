from HskSerial import HskEthernet, HskPacket

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--fwslot", type=int)

args = parser.parse_args()


hsk = HskEthernet()

tio0 = (0, 0x58)
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
surfs = [surf0, surf1, surf2, surf3]


for i in range(0,4): 
    tio = tios[i][1]
    surf = surfs[i]
    hsk.send(HskPacket(tio, 'eEnable', data=[0x40, 0x40]))
    pkt = hsk.receive()
    for j in range(len(surf)):
        val = (surf[j][1])
        hsk.send(HskPacket(val, 'eEnable', data =f"/lib/firmware/{args.fwslot}".encode()))
        pkt = hsk.receive()
        hsk.send(HskPacket(val, 'eRestart', data=[0]))

    