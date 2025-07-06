import os
import time
from checkAuroraBridge import bridgeCheck
import sys
from pueo.turf import PueoTURF
from HskSerial import HskEthernet, HskPacket
from getHSCurrents import checkHSCurrents
from turfManualStartup import turfManualStartup
from surfStartup import surfStartup
from mtsAdvance import mtsAdvance
from checkStartState import checkStartState
#from func_timeout import func_timeout

## First thing is we are going to reset CPU and reboot the TURF
os.system('/home/pueo/pueo-scripts/taylor/ppython /home/pueo/pueo-scripts/ftdi-turf-restart.py --cpu')

## TURF takes like 45 seconds to restart, so we gotta wait
print('rebooting TURF')
time.sleep(70)
print('done')

#dev = PueoTURF()
hsk = HskEthernet()

## Once TURF has rebooted, want to check that the aurora bridge is up and running
## if not, then it hasnt finished rebooting
down = bridgeCheck()
breakout = 0
while (down[0] != 4 and breakout <= 5):
    print('Aurora Bridge is down.')
    for i in down:
        if i == 0:
            hsk.send(HskPacket(0x58, 'eReloadFirmware', data = [0, 0, 0, 0]))
            pkt = hsk.receive()
        if i == 1:
            hsk.send(HskPacket(0x50, 'eReloadFirmware', data = [0, 0, 0, 0]))
            pkt = hsk.receive()
        if i == 2:
            hsk.send(HskPacket(0x40, 'eReloadFirmware', data = [0, 0, 0, 0]))
            pkt = hsk.receive()
        if i == 3:
            hsk.send(HskPacket(0x48, 'eReloadFirmware', data = [0, 0, 0, 0]))
            pkt = hsk.receive()

    print('Reloaded firmware and checking again... ' + str(breakout) + '/5')
    breakout += 1
    down = bridgeCheck()
if (breakout > 5):
    print('Exiting startup...')
    sys.exit(1)

## Checking that the SURFs are in the correct start state
print('Checking SURF start state...')

down = checkStartState(hsk)
if (down != 0):
    print('at least 1 SURF is not in the correct state')
    print('Exiting...')
    sys.exit(1)
    

## Once TURF is ready, we will want to set up TURFIOs
print('Starting up all TURFIOs')
down = turfManualStartup()
if (down != 0):
    print('Failed setting up the TURFIOs')
    print('Exiting...')
    sys.exit(1)
else:
    print('Finished setting up TURFIOs')


## Checking that the SURFs have the correct

'''down = checkHSCurrents()
if (down != 0):
    print('SURF hotswap currents are too low.')
    print('Exiting startup...')
    sys.exit(1)'''


## Aligining SURF clocks
hsk.send(HskPacket(0x40, 'eEnable', [0x40, 0x40]))
hsk.send(HskPacket(0x48, 'eEnable', [0x40, 0x40]))
hsk.send(HskPacket(0x50, 'eEnable', [0x40, 0x40]))
hsk.send(HskPacket(0x58, 'eEnable', [0x40, 0x40]))
#down = surfStartup(tio = 0, slotList = [0, 1, 2, 3, 4, 5, 6])
#if (down == 1):
#    print('SURF failed alignment.')
#    print('Exiting...')
#    sys.exit(1)

down = surfStartup(tio = 1, slotList = [0, 1, 2, 3, 4, 5])
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

## Not set up multi-tile synchronization
print('Setting up multi-tile synchronization...')
down = mtsAdvance(hsk, 0)
down = mtsAdvance(hsk, 1)
down = mtsAdvance(hsk, 2)
down = mtsAdvance(hsk, 3)
print('Multi-tile synchronization complete!')
print('DAQ startup complete!')
print('Ready to take data!')

