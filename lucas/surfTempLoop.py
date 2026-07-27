from HskSerial import HskEthernet, HskPacket
import time

hsk = HskEthernet()

hsk.send(HskPacket(0x48, 'eEnable', data = [0x40, 0x40]))
hsk.receive()
hsk.send(HskPacket(0x58, 'eEnable', data = [0x40, 0x40]))
hsk.receive()
while True:
    time.sleep(1)
    #hsk.send(HskPacket(0xa4,'eTemps')); # Spare
    hsk.send(HskPacket(0x93,'eTemps'));
    print(f"VDAQ: {hsk.receive().pretty()}")
    time.sleep(1)
    #print()
    #hsk.send(HskPacket(0xa3,'eTemps')); # Spare 
    hsk.send(HskPacket(0xa0,'eTemps'));
    print(f"HDAQ: {hsk.receive().pretty()}")
    time.sleep(1)
    hsk.send(HskPacket(0x60,'eTemps')); # TURF
    print(f"TURF: {hsk.receive().pretty()}")
