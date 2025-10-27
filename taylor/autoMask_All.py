# will write script that checks what the status of the thresholds are 
# calibration freeze bullshit
# YOU NEED pyrfdc IN YOUR PYTHONPATH

from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--trigrate", type=int)
parser.add_argument("--removesurf",  type=str)
args = parser.parse_args()

if not args.removesurf:
    removed  =[]
else: 
    removed = list(map(int,args.removesurf.split(',')))


dev = PueoTURF()
premask = dev.trig.mask
for remove in removed:
    premask |= (1 << remove)

print(f'Before: {bin(premask)}')

trigs = dev.trig.scaler.scalers()
surfs = trigs[0:7] + trigs[8:15] + trigs[16:22] + trigs[24:30]
maskoff = []
for i in range(len(surfs)):
    if surfs[i] >= args.trigrate:
        print(f'SURF {i} firing too fast!')
        maskoff.append(i)
if maskoff: 
    print('Masking off!')

for j in range(len(maskoff)):
    premask |= (1 << maskoff[j])

for k in range(27):
    if k not in maskoff and k not in removed:
        premask &= ~(1 << k)

print(f'After: {bin(premask)}')

dev.trig.mask = premask
