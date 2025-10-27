# will write script that checks what the status of the thresholds are 
# calibration freeze bullshit
# YOU NEED pyrfdc IN YOUR PYTHONPATH

from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--trigrate", type=int)
args = parser.parse_args()

dev = PueoTURF()
# need to sample which are masked off already? 
premask = bin(dev.trig.mask())

print(f'Before: {bin(premask)}')

trigs = dev.trig.scaler.scalers()
surfs = trigs[0:7] + trigs[8:15] + trigs[16:22] + trigs[24:30]
maskoff = []
for i in range(len(surfs)): 
    if surfs[i] >= args.trigrate: 
        print(f'SURF {i} firing too fast!')
        print(f'Masking off!')
        maskoff.append(i)

for j in range(len(maskoff)): 
    premask &= ~(1 << maskoff[j])

print(f'After: {bin(premask)}') 

dev.trig.mask = premask 
