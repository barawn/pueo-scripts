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
print("SURF Software: ", idList[3])
# technically there's more crap
for l in range(len(idList[4:])):    
    print(f'Field {l+4}: {idList[l+4]}')

print("Next Firmware: ", fwPkt.data.decode())

