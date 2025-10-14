import argparse
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF

parser = argparse.ArgumentParser()

parser.add_argument("--nbeams", type=int, default=46)
parser.add_argument("--tio", type=int, default=3)
parser.add_argument("--showUpdate", action="store_true")
parser.add_argument("--showPeriod", action="store_true")

args = parser.parse_args()

dev =PueoTURF()
tio=PueoTURFIO((dev,args.tio),'TURFGTP')
surf=PueoSURF((tio,6),'TURFIO')
for i in range(args.nbeams):
    rate=surf.levelone.read(0x400+4*i)
    trigger_rate = rate & 0x0000FFFF
    subthreshold_rate = (rate & 0xFFFF0000) >> 16
    print(f"T{i:02d}:{trigger_rate:7d}  S{i:02d}:{subthreshold_rate:7d}"," ",end="")
    if (i % 5 == 4): 
        print()
print()
if(args.showUpdate):
    print(f"Update Toggle:{surf.levelone.read(0x1804)}")
if(args.showPeriod):
    print(f"Update Period:{surf.levelone.read(0x1808)/(1.0e8)} s")
