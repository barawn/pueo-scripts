from HskSerial import HskEthernet, HskPacket

hsk = HskEthernet()
hsk.send(HskPacket(0x48, 'eEnable', [0x40, 0x40])); pkt = hsk.receive()
hsk.send(HskPacket(0xa3, 'eSleep', data = [0x85])); pkt = hsk.receive()
hsk.send(HskPacket(0x9c, 'eSleep', data = [0x85])); pkt = hsk.receive()
hsk.send(HskPacket(0x48, 'eEnable', [0x40, 0x00])); pkt = hsk.receive()