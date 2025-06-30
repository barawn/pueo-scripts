from HskSerial import HskEthernet, HskPacket
import sys

tio_addr = [0x40, 0x48, 0x50, 0x58]


def checkHSCurrents():
    down = []
    hsk = HskEthernet()
    for addr in tio_addr:
        hsk.send(HskPacket(addr, 'eCurrents'))
        data = hsk.receive().data
        for iter in range(0, 16, 2):
            val = (int.from_bytes(data[iter:iter+2], byteorder='big') )
            if (iter==0):
                I = val*105.84/(2**12*0.125)
                print('TURFIO:', round(I, 2), 'mA')
            else:
                I = (val - 2048)*12.51/4.762
                if (I > 0):
                    print('SURF slot ' + str(int(iter/2)) + ':', round(I, 2), 'mA')
                if (I < 450):
                    print('SURF slot ' + str(str(int(iter/2))) + ' on TURFIO at address ' + str(addr) + 'did not boot correctly')
                    down.append((addr,iter/2))
    if (len(down) != 0):
        return down

    return 0