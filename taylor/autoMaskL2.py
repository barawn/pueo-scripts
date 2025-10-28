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
    premask |= (1 << remove) # this is to remove surfs manually 

print(f'Before: {bin(premask)}')

l1trigs = dev.trig.scaler.scalers()
l2surfs = dev.trig.scaler.leveltwos()
l1surfs = l1trigs[0:7] + l1trigs[8:15] + l1trigs[16:22] + l1trigs[24:30]
l2rate = sum(l2surfs)
print(f'Reported L2 Triggers: {l2rate}')

maskoff = []

if l2rate >= args.trigrate: 
    maxVal = max(l2surfs)
    adjIndices = [maxVal - 1, maxVal, maxVal + 1]
    maxIndex = max(adjIndices, key=lambda i: l1surfs[i])
    maxL1Trig = l1surfs[maxIndex]
    for i in adjIndices:
        print(f"SURF Value {l1surfs[i]}")
    print(f'Max L1 trigger found: {maxL1Trig}, gotta mask that off')
    maskoff.append(maxIndex)

    
"""for i in range(len(l1surfs)):
    if l1surfs[i] >= args.trigrate:
        print(f'SURF {i} firing too fast!')
        maskoff.append(i)
if maskoff: 
    print('Masking off!')"""

for j in range(len(maskoff)):
    premask |= (1 << maskoff[j])

for k in range(27):
    if k not in maskoff and k not in removed:
        premask &= ~(1 << k)

print(f'After: {bin(premask)}')

dev.trig.mask = premask
