import os
import time

## First thing is we are going to reset CPU and reboot the TURF
os.system('../ftdi-turf-restart.py')

## TURF takes like 45 seconds to restart, so we gotta wait
time.sleep(60)




