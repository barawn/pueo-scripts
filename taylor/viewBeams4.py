from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF

dev =PueoTURF()
tio=PueoTURFIO((dev,3),'TURFGTP')
surf=PueoSURF((tio,4),'TURFIO')
for i in range(46):
    rate=surf.levelone.read(0x400+4*i)
    print(f"{rate:7d}"," ",end="")
    if (i % 10 == 9): 
        print()
print()
