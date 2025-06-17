
from HskSerial import HskEthernet, HskPacket


print('Aye Aye, Captain!')

hsk = HskEthernet()
hsk.send(HskPacket(0x40, 'eEnable', [0x40, 0x40]))
pkt = hsk.receive()
hsk.send(HskPacket(0x48, 'eEnable', [0x40, 0x40]))
pkt = hsk.receive()
hsk.send(HskPacket(0x50, 'eEnable', [0x40, 0x40]))
pkt = hsk.receive()
hsk.send(HskPacket(0x58, 'eEnable', [0x40, 0x40]))
pkt = hsk.receive()

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

print('Aye Aye, Captain!')


