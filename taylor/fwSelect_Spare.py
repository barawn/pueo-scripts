from HskSerial import HskEthernet, HskPacket

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--fwslot", type=int)
parser.add_argument("--slots", type=str, default='3,6')
hsk = HskEthernet()
args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))

tio = (0, 0x48)
surf1 = [ 
        (3, 0x9c),
        (6, 0xa3) ]

tio = tio[1]
hsk.send(HskPacket(tio, 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()

for slot in slotList: 
    newsurf = dict(surf1)
    surf = newsurf[slot]
    hsk.send(HskPacket(surf, 'eFwNext', data =f"/lib/firmware/{args.fwslot}".encode()))
    pkt = hsk.receive().data
    if pkt == b'':
        print(f'SURF Slot {slot} sent eError... no /mnt/bitstream/{args.fwslot}')
    else:
        hsk.send(HskPacket(surf, 'eRestart', data=[0]))