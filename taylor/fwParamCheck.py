from HskSerial import HskEthernet, HskPacket
import time
import csv
from datetime import datetime

filename = 'fwParam_v0r6p32.csv'

hsk = HskEthernet()
headers = [ 'tio', 'slot', 'rxclk', 'cin', 'cin bit']

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


hsk.send(HskPacket(0x48, 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()
hsk.send(HskPacket(0x40, 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()
hsk.send(HskPacket(0x58, 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()
hsk.send(HskPacket(0x50, 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()


with open(filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(headers)
    for i in range(0,4): 
        tio = tios[i][1]
        surf = surfs[i]
        
        for j in range(len(surf)):
            val = (surf[j][1])
            hsk.send(HskPacket(val, 'eFwParams', data =[0]))
            data = hsk.receive().data
            
            rxclk = ((int.from_bytes(data[0:4],byteorder='big')))
            cin = ((int.from_bytes(data[4:8],byteorder='big'))/1000)
            cinBit = (int.from_bytes(data[8:9],byteorder='big'))
            
            new_data = [ i, j, rxclk, cin, cinBit ]
            csv_writer.writerow(new_data)
