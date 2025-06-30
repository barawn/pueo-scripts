import os
import time
from checkAuroraBridge import bridgeCheck
import sys
from pueo.turf import PueoTURF
from HskSerial import HskEthernet
from getHSCurrents import getHSCurrents()

## First thing is we are going to reset CPU and reboot the TURF
os.system('/home/pueo/taylor/ppython /home/pueo/pueo-scripts/ftdi-turf-restart.py --cpu')

## TURF takes like 45 seconds to restart, so we gotta wait
time.sleep(60)

dev = PueoTURF()
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
os.system('/home/pueo/taylor/ppython /home/pueo/startup/turfManualStartup.py')

## Checking that the SURFs have the correct
down = getHSCurrents()
if (down != 0):
    print('SURF hotswap currents are too low.')
    print('Exiting startup...')
    sys.exit(1)