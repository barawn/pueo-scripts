from HskSerial import HskEthernet, HskPacket

hsk = HskEthernet()
tios = [0x40, 0x48, 0x50, 0x58]

for tio in tios:
    hsk.send((HskPacket(tio , 'eEnable', [0x40, 0x40])))