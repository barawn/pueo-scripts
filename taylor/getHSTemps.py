import argparse
from HskSerial import HskEthernet, HskPacket

parser = argparse.ArgumentParser()
parser.add_argument('addr',
                    help='housekeeping address of TURFIO to get Hot Swap currents of RACK',
                    type=lambda x : int(x,0))
args = parser.parse_args()


hsk = HskEthernet()
hsk.send(HskPacket(args.addr, 'eTemps'))
data = hsk.receive().data
#data = b"\x06'\x08\x87\t\xf9\t\xf6\t\xfb\t\xf9\t\xf4\t\xf1"
currents = []
if args.addr == 0x40 or args.addr == 0x48:
    R = 14
else:
    R = 16
for iter in range(0, R, 2):
    val = (int.from_bytes(data[iter:iter+2], byteorder='big') )
    if (iter==0):
        T = val*503.975/(2**12) - 273.15
        print('TURFIO:', round(T, 2), 'C')
    else:
        T = (val*10 - 31880)/42
        print('SURF slot ' + str(int(iter/2)) + ':', round(T, 2), 'C')