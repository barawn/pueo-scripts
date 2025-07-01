from HskSerial import HskEthernet, HskPacket
import time


def checkStartState(hsk): 

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
            (6, 0x9c)]

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
            (2, 0x96),
            (3, 0x8e),
            (4, 0x90),
            (5, 0x92) ]
    
    tios = [tio0, tio1, tio2, tio3]
    surfs = [surf0, surf1, surf2, surf3]

    tios, surfs = addr()
    failed = []
    for tio in tios: 
        hsk.send(HskPacket(tio[1], 'eEnable', data = [0x40, 0x40]))
        pkt = hsk.receive()
        idx = tios.index(tio)
        for surf in surfs[idx]:
            pkt = 0 
            hsk.send(HskPacket(surf[1], 'eStartState'))
            try:
                pkt = hsk.receive().data
                if pkt is None:
                    failed.append((tio[1], surf[0]))
                    print('failed to receive a response')
            except: 
                print(pkt) 
                continue 
    



    """hsk.send(HskPacket(0x40, 'eEnable', [0x40, 0x40]))
    pkt = hsk.receive()
    hsk.send(HskPacket(0x48, 'eEnable', [0x40, 0x40]))
    pkt = hsk.receive()
    hsk.send(HskPacket(0x50, 'eEnable', [0x40, 0x40]))
    pkt = hsk.receive()
    hsk.send(HskPacket(0x58, 'eEnable', [0x40, 0x40]))
    pkt = hsk.receive()

    print("Are you Ready kids?")"""
"""
    surfs = [ (0, 0x97),
            (1, 0xa0),
            (2, 0x99),
            (3, 0x8d),
            (4, 0x9d),
            (5, 0x94),
            (6, 0x8a),
            (0, 0x8c),
            (1, 0x95),
            (2, 0x9f),
            (3, 0x9a),
            (4, 0x87),
            (5, 0x85), 
            (6, 0x9c),
            (0, 0x89),
            (1, 0x88),
            (2, 0x9e),
            (3, 0x8b),
            (4, 0xa1),
            (5, 0x98),
            (0, 0x93),
            (1, 0x9b),
            (2, 0x96),
            (3, 0x8e),
            (4, 0x90),
            (5, 0x92)]

    for ii in range(len(surfs)):
        hsk.send(HskPacket(surfs[ii][1], 'eStartState'))
        rm = hsk.receive()
        print(rm.pretty())

    print('Aye Aye, Captain!')"""

checkStartState(1)