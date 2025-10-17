from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF 
import time

dev = PueoTURF()
tio = PueoTURFIO((dev, 0), 'TURFGTP')
surf = PueoSURF((tio, 6), 'TURFIO')

print('Unmask All and Wait 5s')
surf.levelone.write(0x2008, 0x00000)
surf.levelone.write(0x200C, 0x8000000)
time.sleep(5) 
dev.trig.scaler.scalers(verbose = True) 



print('Mask All and Wait 5s Attempt 1')
surf.levelone.write(0x2008, 0xFFFFF)
surf.levelone.write(0x200C, 0xFFFFFFF)
time.sleep(5) 
dev.trig.scaler.scalers(verbose = True)


print('Mask All and Wait 5s Attempt 2')
surf.levelone.write(0x2008, 0xFFFFF)
surf.levelone.write(0x200C, 0xFFFFFFF)
time.sleep(5) 
dev.trig.scaler.scalers(verbose = True)

