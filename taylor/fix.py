#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket

ls = [ 0x97, 0xa0, 0x99, 0x8d, 0x9d, 0x94, 0x8a ]

hsk = HskEthernet()

for s in ls:
    hsk.send(HskPacket(s, 'eFwNext', data='/lib/firmware/pueo_surf6_v0r1p13.bit'.encode()))
    print(hsk.receive().pretty(asString=True))

