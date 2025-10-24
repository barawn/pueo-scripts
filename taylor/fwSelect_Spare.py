from HskSerial import HskEthernet, HskPacket

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--fwslot", type=int)
hsk = HskEthernet()
args = parser.parse_args()

tio = (0, 0x48)
surf = [ 
        (3, 0x9c),
        (6, 0xa3) ]

tio = tio[1]
hsk.send(HskPacket(tio, 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()
for j in range(len(surf)):
    hsk.send(HskPacket(surf[j][1], 'eFwNext', data =f"/lib/firmware/{args.fwslot}".encode()))
    pkt = hsk.receive()
    hsk.send(HskPacket(surf[j][1], 'eRestart', data=[0]))