from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF

dev =PueoTURF()
tio=PueoTURFIO((dev,0),'TURFGTP')
surf=PueoSURF((tio,6),'TURFIO')
for i in range(8): #loop over channels
    done=surf.levelone.read(0x4000+0x4004*i)
    sqr=surf.levelone.read(0x4004+0x400*i)/65536
    gt=surf.levelone.read(0x4008+0x400*i)/65536
    lt=surf.levelone.read(0x400c+0x400*i)/65536
    scale=surf.levelone.read(0x4010+0x400*i)
    offset=surf.levelone.read(0x4014+0x400*i)
    print(f"Slot 6 Ch {i:2} Var:{sqr:11.3e} GT:{gt:11.3e} LT:{lt:11.3e} Scale:{scale:11d} Offset:{offset:11d}")
surf2=PueoSURF((tio,5),'TURFIO')
for i in range(8): #loop over channels
    done=surf2.levelone.read(0x4000+0x4004*i)
    sqr=surf2.levelone.read(0x4004+0x400*i)/65536
    gt=surf2.levelone.read(0x4008+0x400*i)/65536
    lt=surf2.levelone.read(0x400c+0x400*i)/65536
    scale=surf2.levelone.read(0x4010+0x400*i)
    offset=surf2.levelone.read(0x4014+0x400*i)
    print(f"Slot 3Ch {i:2} Var:{sqr:11.3e} GT:{gt:11.3e} LT:{lt:11.3e} Scale:{scale:11d} Offset:{offset:11d}")
