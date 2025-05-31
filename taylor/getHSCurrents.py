import argparse
from HskSerial import HskEthernet, HskPacket

parser = argparse.ArgumentParser()
parser.add_argument('addr',
                    help='housekeeping address of TURFIO to get Hot Swap currents of RACK',
                    type=lambda x : int(x,0))
args = parser.parse_args()


hsk = HskEthernet()
hsk.send(HskPacket(args.addr, 'eCurrents'))
data = hsk.receive().data
#data = b"\x06'\x08\x87\t\xf9\t\xf6\t\xfb\t\xf9\t\xf4\t\xf1"
currents = []
for iter in range(0, 16, 2):
    val = (int.from_bytes(data[iter:iter+2], byteorder='big') )
    if (iter==0):
        I = val*105.84/(2**12*0.125)
        print('TURFIO:', round(I, 2), 'mA')
    else:
        I = (val - 2048)*12.51/4.762
        print('SURF slot ' + str(int(iter/2)) + ':', round(I, 2), 'mA')