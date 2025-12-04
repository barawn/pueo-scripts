from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--tio", type=int)
parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")


args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))


dev = PueoTURF(None, 'Ethernet')

tio = PueoTURFIO((dev, args.tio), 'TURFGTP')


for slot in slotList: 
    surf = PueoSURF((tio, slot), 'TURFIO')
    for i in range(8): #loop over channels
        done=surf.levelone.read(0x4000+0x4004*i)
        sqr=surf.levelone.read(0x4004+0x400*i)/65536
        gt=surf.levelone.read(0x4008+0x400*i)/65536
        lt=surf.levelone.read(0x400c+0x400*i)/65536
        scale=surf.levelone.read(0x4010+0x400*i)
        offset=surf.levelone.read(0x4014+0x400*i)
        if offset > 65536/2:
            offset -= 65536/2
        print(f"Slot {slot} Ch {i:2} Var:{sqr:11.3e} GT:{gt:11.3e} LT:{lt:11.3e} Scale:{scale:11f} Offset:{offset:11f}")
    print("")
 
