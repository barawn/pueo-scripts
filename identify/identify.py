#!/usr/bin/env python3

from HskSerial import HskSerial, HskEthernet, HskPacket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--local',
                    action='store_true',
                    help='set to 1 if using /dev/hsklocal')
parser.add_argument('addr',
                    help='housekeeping address of SURF to identify',
                    type=lambda x : int(x,0))
args, remaining = parser.parse_known_args()
addr = args.addr
cmdstr = ' '.join(remaining)
if args.local:
    hsk = HskSerial('/dev/hsklocal', srcId=0xFC)
else:
    hsk = HskEthernet()
hsk.send(HskPacket(addr, 'eIdentify'))
idPkt = hsk.receive()
hsk.send(HskPacket(addr, 'eFwNext'))
fwPkt = hsk.receive()

idList = idPkt.data.decode().split('\x00')
idLen = len(idList)
print("DNA: ", idList[0])
print("MAC: ", idList[1])
print("PetaLinux: ", idList[2])
# Those are always there. Next grab SW version if possible.
if len(idList[3:6]) == 3:
    print(f'SURF Software: {idList[3]} hash {idList[4]} date {idList[5]}')
    idx = 6
else:
    idx = 3
if len(idList[idx:idx+1]):
    print(f'Location: {idList[idx:]}')

print("Next Firmware: ", fwPkt.data.decode())

