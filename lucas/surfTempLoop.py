from HskSerial import HskEthernet, HskPacket
import time

hsk = HskEthernet()
hsk.send(HskPacket(0x48, 'eEnable', data = [0x40, 0x40]))
hsk.receive()
while True:
    time.sleep(1)
    hsk.send(HskPacket(0x9c,'eTemps')); 
    print(hsk.receive().pretty())
    hsk.send(HskPacket(0xa3,'eTemps')); 
    print(hsk.receive().pretty())
