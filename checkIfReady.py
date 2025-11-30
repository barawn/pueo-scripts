import sys
import argparse 
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF

parser = argparse.ArgumentParser()
parser.add_argument("--tio", type=str, default="0,1,2,3", 
        help="comma-separated list of TURFIOs to initialize")
parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))

if args.tio == '0':
    tios = (0, 0x58)
    surfs = [ (0, 0x97),
            (1, 0xa0),
            (2, 0x99),
            (3, 0x8d),
            (4, 0x9d),
            (5, 0x94),
            (6, 0x8a) ]
elif args.tio == '1':
    tios = (1, 0x50)
    surfs = [ (0, 0x8c),
            (1, 0x95),
            (2, 0x9f),
            (3, 0x9a),
            (4, 0x87),
            (5, 0x85), 
            (6, 0x91)]
elif args.tio == '2':
    tios = (2, 0x40)
    surfs = [ (0, 0x89),
            (1, 0x88),
            (2, 0x9e),
            (3, 0x8b),
            (4, 0xa1),
            (5, 0x98)]
elif args.tio == '3':
    tios = (3, 0x48)
    surfs = [ (0, 0x93),
            (1, 0x9b),
            (2, 0x86),
            (3, 0x8e),
            (4, 0x90),
            (5, 0x92) ]
elif args.tio == 't':
    tios = (3, 0x48)
    surfs = [ (0, 0x93) ]


dev = PueoTURF()
 
tio = PueoTURFIO((dev, tios[0]), 'TURFGTP')

for s in slotList:
    val = (surfs[s][0])
    try:
        surf = PueoSURF((tio, val), 'TURFIO')
    except: 
        print('RX clock off')
        sys.exit()
    
    lolval = surf.lol 
    rftrig = surf.trig_clock_en
    if lolval == 1 or rftrig == 0: 
        print('Clock not on correctly! Restart recommended')
        sys.exit()
    else: 
        continue 

print('All trigger clocks are reporting on and no LOL')

