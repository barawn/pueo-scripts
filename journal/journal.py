#!/usr/bin/env python3

from HskSerial import HskSerial, HskEthernet, HskPacket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--local',
                    help='set to 1 if using /dev/hsklocal')
parser.add_argument('addr',
                    help='housekeeping address of SURF to get journal from',
                    type=lambda x : int(x,0))
args, remaining = parser.parse_known_args()
addr = args.addr
cmdstr = ' '.join(remaining)
print(f'Sending eJournal to {hex(addr)}: journalctl {cmdstr}')

if args.local:
    hsk = HskSerial('/dev/hsklocal', srcId=0xFC)
else:
    hsk = HskEthernet()
hsk.send(HskPacket(addr, 'eJournal', data=cmdstr.encode()))

res = ''
pkt = hsk.receive()
res += pkt.data.decode()
while len(pkt.data) == 255:
    hsk.send(HskPacket(addr, 'eJournal'))
    pkt = hsk.receive()
    res += pkt.data.decode()

lines = res.split('\n')
for line in lines:
    print(line)

