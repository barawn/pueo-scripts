import argparse
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
hsk.send(HskPacket(args.addr, 'eEnable', [0x40, 0x40]))
hsk.send(HskPacket(args.addr, 'eTemps'))
data = hsk.receive().data

currents = []
for iter in range(len(surfs)):
    hsk.send(HskPacket(surfs[iter], 'eTemps'))
    data = hsk.receive().data
    val = (int.from_bytes(data[iter:iter+2], byteorder='big') )
    T = (val*10 - 31880)/42
    print('SURF slot ' + str(int(iter/2)) + ':', round(T, 2), 'C')