import argparse
import sys
from HskSerial import HskEthernet, HskPacket

parser = argparse.ArgumentParser()
parser.add_argument('addr',
                    help='housekeeping address of TURFIO to get APU temperatures of RACK',
                    type=lambda x : int(x,0))
args = parser.parse_args()

if (args.addr == 0x58):
    # SURFs in Hpol LRACK --> SOCID
    surfs = [ 0x97, 0xa0, 0x99, 0x8d, 0x9d, 0x94, 0x8a ]
elif (args.addr == 0x50):
    # SURFs in Hpol RRACK --> SOCID
    surfs = [ 0x8c, 0x95, 0x9f, 0x9a, 0x87, 0x85, 0x9c ] 
elif(args.addr == 0x48):
    # SURFs in Vpol LRACK --> SOCID
    surfs = [ 0x93, 0x9b, 0x96, 0x8e, 0x90, 0x92 ]
elif(args.addr == 0x40): 
    # SURFs in Vpol RRACK --> SOCID
    surfs = [ 0x89, 0x88, 0x9e, 0x8b, 0xa1, 0x98 ] 

hsk = HskEthernet()

#check if surfs are ready --> good startup state
iter = 0
for s in surfs:
    iter = iter + 1
    hsk.send(HskPacket(s, 'eStartState'))
    pkt = hsk.receive().data
    state = int.from_bytes(pkt,byteorder='big')
    print('SURF in slot {} is in state {}'.format(iter, state))
