import os
import time
from checkAuroraBridge import bridgeCheck
import sys
from pueo.turf import PueoTURF
from HskSerial import HskEthernet
from getHSCurrents import checkHSCurrents
from turfManualStartup import turfManualStartup
from surfStartup import surfStartup

## First thing is we are going to reset CPU and reboot the TURF
os.system('/home/pueo/pueo-scripts/taylor/ppython /home/pueo/pueo-scripts/ftdi-turf-restart.py --cpu')

## TURF takes like 45 seconds to restart, so we gotta wait
print('rebooting TURF')
time.sleep(60)
print('done')

#dev = PueoTURF()
hsk = HskEthernet()

## Once TURF has rebooted, want to check that the aurora bridge is up and running
## if not, then it hasnt finished rebooting
down = bridgeCheck()
if (down[0] != 4):
    print('Aurora Bridge is down.')
    print('Exiting startup...')
    sys.exit(1)
    

## Once TURF is ready, we will want to set up TURFIOs
print('Starting up all TURFIOs')
down = turfManualStartup()
if (down != 0):
    print('Failed setting up the TURFIOs')
    sys.exit(1)
else:
    print('Finished setting up TURFIOs')


## Checking that the SURFs have the correct
down = checkHSCurrents()
if (down != 0):
    print('SURF hotswap currents are too low.')
    print('Exiting startup...')
    sys.exit(1)

down = surfStartup(tio = 0, slotList = [0, 1, 2, 3, 4, 5, 6])
if (down == 1):
    print('SURF failed alignment.')
    print('Exiting...')
    sys.exit(1)
down = surfStartup(tio = 1, slotList = [0, 1, 2, 3, 4, 5, 6])
if (down == 1):
    print('SURF failed alignment.')
    print('Exiting...')
    sys.exit(1)
down = surfStartup(tio = 2, slotList = [0, 1, 2, 3, 4, 5])
if (down == 1):
    print('SURF failed alignment.')
    print('Exiting...')
    sys.exit(1)
down = surfStartup(tio = 3, slotList = [0, 1, 2, 3, 4, 5])
if (down == 1):
    print('SURF failed alignment.')
    print('Exiting...')
    sys.exit(1)

