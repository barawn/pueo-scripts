import sys
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF


tio0 = (0, 0x58)
surf0 = [ (0, 0x97),
        (1, 0xa0),
        (2, 0x99),
        (3, 0x8d),
        (4, 0x9d),
        (5, 0x94),
        (6, 0x8a) ]

tio1 = (1, 0x50)
surf1 = [ (0, 0x8c),
        (1, 0x95),
        (2, 0x9f),
        (3, 0x9a),
        (4, 0x87),
        (5, 0x85), 
        (6, 0x91)]

tio2 = (2, 0x40)
surf2 = [ (0, 0x89),
        (1, 0x88),
        (2, 0x9e),
        (3, 0x8b),
        (4, 0xa1),
        (5, 0x98)]

tio3 = (3, 0x48)
surf3 = [ (0, 0x93),
        (1, 0x9b),
        (2, 0x86),
        (3, 0x8e),
        (4, 0x90),
        (5, 0x92) ]

tios = [tio0, tio1, tio2, tio3]
surfs = [surf0, surf1, surf2, surf3]
dev = PueoTURF()

for i in range(0,4): 
    tio = PueoTURFIO((dev, i), 'TURFGTP')
    print(i)
    surfv = surfs[i] 
    for j in range(len(surfv)):
        val = (surfv[j][0])
        print(j)
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

