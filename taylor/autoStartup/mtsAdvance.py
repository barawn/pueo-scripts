#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import time 

def mtsAdvance(hsk, tio = '0'):
    if isinstance(tio, int):
        tio = str(tio)

    if tio == '0':
        tios = (0, 0x58)
        surfs = [ (0, 0x97),
                (1, 0xa0),
                (2, 0x99),
                (3, 0x8d),
                (4, 0x9d),
                (5, 0x94)]
    elif tio == '1':
        tios = (1, 0x50)
        surfs = [ (0, 0x8c),
                (1, 0x95),
                (2, 0x9f),
                (3, 0x9a),
                (4, 0x87),
                (5, 0x85)]
    elif tio == '2':
        tios = (2, 0x40)
        surfs = [ (0, 0x89),
                (1, 0x88),
                (2, 0x9e),
                (3, 0x8b),
                (4, 0xa1),
                (5, 0x98)]
    elif tio == '3':
        tios = (3, 0x48)
        surfs = [ (0, 0x93),
                (1, 0x9b),
                (2, 0x96),
                (3, 0x8e),
                (4, 0x90),
                (5, 0x92) ]
    elif tio == 't':
        tios = (3, 0x48)
        surfs = [ (0, 0x93) ]

    #if (slotmaskoff != None):
    #    for s in slotmaskoff:
    #        try:
    #            surfs.remove(surfs[s])
    #            print(surfs)
    #        except:
    #            print(f'TURFIO does not have a slot {s}')


    #hsk = HskEthernet()
    hsk.send(HskPacket(tios[1], 'eEnable', data=[0x40, 0x40]))
    pkt = hsk.receive()
    print('This takes 5 seconds to run! Be patient!')
    for s in surfs:
        hsk.send(HskPacket(s[1], 'eFwParams', data = b'\x01\x00\x00\x00\x78\x00'))
        pkt = hsk.receive()
        hsk.send(HskPacket(s[1], 'eStartState', data=[19])) 
        pkt = hsk.receive()
    time.sleep(5)
    for s in surfs:
        hsk.send(HskPacket(s[1], 'eStartState'))
        pkt = hsk.receive()
        print(pkt.pretty())

    return 0
