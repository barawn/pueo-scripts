#!/usr/bin/env python3

from pueo.turf import PueoTURF
from EventTester import EventServer


dev = PueoTURF()
es = EventServer()

# Check if events are running already
if dev.trig.running == 1: 
    es.close()
    dev.trig.runcmd(dev.trig.RUCNMD_STOP)

dev.trig.mask = 268435455 # masks off all SURFs (LF + MI)

es.open()
dev.trig.runcmd(dev.trig.RUNCMD_RESET)