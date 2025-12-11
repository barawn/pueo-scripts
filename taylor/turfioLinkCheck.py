from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
import sys

dev = PueoTURF()

for i in range(4): 
    try:
        tio = PueoTURFIO((dev,i), 'TURFGTP')
    except:
        print(f'TURFIO PORT#{i} link failed')
        sys.exit

print('All TURFIO links found!')
