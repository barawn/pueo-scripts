import sys
import argparse
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF

parser = argparse.ArgumentParser()
parser.add_argument("--tio", type=int)
parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")
args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))

dev = PueoTURF()
tio = PueoTURFIO((dev, args.tio), 'TURFGTP')
rxClockOff = 0 # counter for how many times

# we can just use straight up the slot list since its solely
# register space
for slot in slotList:
    try: # try to create a SURF object... will throw error for rxclk off 
        surf = PueoSURF((tio, slot), 'TURFIO')
    except:
        rxClockOff += 1
if rxClockOff == len(slotList):
    print('RX clock off on all SURFs')
    sys.exit() # reported for all SURFs
elif rxClockOff != len(slotList) and rxClockOff != 0:
    print('RX clock off on only a few SURFs. Restart recommended!')
    sys.exit() # reported for a few SURFs to catch a half started crate

# If you get to here, check for lol and that the trigger clock is enabled
for slot in slotList:
    surf = PueoSURF((tio,slot), 'TURFIO') # change the SURF to look at everything
    lolval = surf.lol
    rftrig = surf.trig_clock_en
    if lolval == 1 or rftrig == 0:
        print('Clock not on correctly! Restart recommended')
        sys.exit() # exit immediately if no because you'll need to reboot
    else:
        continue
print('All trigger clocks are reporting on and no LOL')

