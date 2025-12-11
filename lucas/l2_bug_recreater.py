#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from EventTester import EventServer
import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--stop', type=int) 
parser.add_argument('--filename')
parser.add_argument('--orlogic', action='store_true')
parser.add_argument('--maskLF', action='store_true')
parser.add_argument('--pickupFSW', action='store_true')
parser.add_argument('--blitzThenLower', action='store_true')
args = parser.parse_args()

dev = PueoTURF()
es = EventServer()

## LUCAS EDIT HERE FOR THE THRESHOLDS
thresholdOR = 7000
thresholdAND = 6500


for i in range(4):
    tio = PueoTURFIO((dev, i), 'TURFGTP')
    if i == 0 or i == 1: 
        for s in range(6):
            surf = PueoSURF((tio, s), 'TURFIO')#6500
            if surf.trig_clock_en != 1 : 
                print("Yo, the RF stuff ain't set up right")
                sys.exit()
            if(not args.pickupFSW):
                if(args.orlogic):
                    dev.trig.leveltwo_logic = 1
                    for i in range(48): 
                        surf.levelone.write(0x800 + i*4,thresholdOR) #
                    surf.levelone.write(0x1800, 2)# Apply new thresholds
                else:
                    dev.trig.leveltwo_logic = 0
                    for i in range(48): 
                        surf.levelone.write(0x800 + i*4,thresholdAND) #
                    surf.levelone.write(0x1800, 2)# Apply new thresholds
    else:
        for s in range(6): 
            surf = PueoSURF((tio, s), 'TURFIO')#6500
            if surf.trig_clock_en != 1 : 
                print("Yo, the RF stuff ain't set up right")
                sys.exit()
            if(not args.pickupFSW):
                if(args.orlogic):
                    dev.trig.leveltwo_logic = 1
                    for i in range(48): 
                        surf.levelone.write(0x800 + i*4,thresholdOR) #
                    surf.levelone.write(0x1800, 2)# Apply new thresholds 
                else:
                    dev.trig.leveltwo_logic = 0
                    for i in range(48): 
                        surf.levelone.write(0x800 + i*4,thresholdAND) #
                    surf.levelone.write(0x1800, 2)# Apply new thresholds 

if(args.maskLF):
    dev.trig.mask = 0b110000000000000000000000000
else:
    dev.trig.mask = 0b000000000000000000000000000

if(not args.pickupFSW):
    dev.trig.mask = 0
    if(args.orlogic):
        dev.trig.leveltwo_logic = 1
    else:
        dev.trig.leveltwo_logic = 0
else:
    print(f"Started with {dev.trig.mask} mask and {dev.trig.leveltwo_logic} L2 logic reg")

es.open()
dev.trig.runcmd(dev.trig.RUNCMD_RESET)
#dev.evstatus()
startCount = dev.trig.trigger_count
start = time.time()
L2_begin = dev.trig.scaler.leveltwos()
last100 = L2_begin
for i in range(args.stop):
    print(i)
    print(f"Trig count:{dev.trig.trigger_count}")
    print(dev.trig.scaler.leveltwos())
    if(i % 100 == 99):
        print(f'Mid Run L2: {dev.trig.scaler.leveltwos()}')
        print(f'Event number {i}')
        print(f'Average rate so far: {100.0/(time.time() - last100)}')
        last100 = time.time()
    e = es.event_receive()
    f = open(f'{args.filename}_{i}.pkl', 'wb')
    pickle.dump(e,f)
    f.close()
endCount = dev.trig.trigger_count
end = time.time()
L2_end = dev.trig.scaler.leveltwos()

if(args.maskLF):
    print("MASKING LF")
if(args.orlogic):
    print("USING L1 (OR) LOGIC")
else:
    print("USING L2 (AND) LOGIC")
print(f"Time delta: {end-start} s")
print(f"Measured Rate: {args.stop/(end-start)} Hz")
print(f"Trig delta: {endCount - startCount}")
print(f"L2_begin: {L2_begin}")
print(f"L2_end: {L2_end}")

for i in range(449):
    es.es.recv(1032)

es.close()
dev.trig.runcmd(dev.trig.RUNCMD_STOP)
print('REGISTER READ TIME, YO!')
print(f'TURFIO MASK: {dev.event.mask}')
print(f'FRAGMENT SIZE: {es.max_fragment}')
print(f'FRAGMENT SOURCE MASK: {es.max_mask}') 
print(f'PPS ENABLED: {dev.trig.pps_trig_enable}')
print(f'PPS OFFSET: {dev.trig.pps_offset}') 
print(f'RF OFFSET: {dev.trig.offset}') 
print(f'RF ENABLE: {dev.trig.rf_trig_en}') 
print(f'SOFTWARE TRIGGER: I think this one is set only flight software... sorry') 
print(f'LF MASKING: {dev.trig.mask}') 
print(f'PHOTOSHUTTER ENABLE: {dev.trig.photo_en}') 
print(f'PHOTOSHUTTER PRESCALE: {dev.trig.photo_prescale}') 
print(f'MASK AGAIN: {dev.trig.mask}') 
print(f'THRESHOLDS: {surf.levelone.read(0x800)}')
print(f'SUBTHRESHOLDS: {surf.levelone.read(0xA00)}') 
print(f'RUNDLY (for fun!): {dev.trig.rundly}')
with open(args.filename, "w") as outfile:
    outfile.write(f"TURFIO MASK: {dev.event.mask}\nFRAGMENT SIZE: {es.max_fragment}\nFRAGMENT SOURCE MASK: {es.max_mask}\n PPS ENABLE: {dev.trig.pps_trig_enable}\nPPS OFFSET: {dev.trig.pps_offset}\nRF OFFSET: {dev.trig.offset}\nRF ENABLE: {dev.trig.rf_trig_en}\nLF MASKING: {dev.trig.mask}\n PHOTOSHUTTER ENABLE: {dev.trig.photo_en}\nPHOTOSHUTTER PRESCALE: {dev.trig.photo_prescale}\nMASK AGAIN: {dev.trig.mask}\nTHRESHOLDS: {surf.levelone.read(0x800)}\nSUBTHRESHOLDS: {surf.levelone.read(0xA00)}\n")


if(args.blitzThenLower):
    ## LUCAS EDIT HERE FOR THE THRESHOLDS
    thresholdOR_BLITZ = 8000
    thresholdAND_BLITZ = 2500


    for i in range(4):
        tio = PueoTURFIO((dev, i), 'TURFGTP')
        if i == 0 or i == 1: 
            for s in range(7):
                surf = PueoSURF((tio, s), 'TURFIO')#6500
                if surf.trig_clock_en != 1 : 
                    print("Yo, the RF stuff ain't set up right")
                    sys.exit()
                if(not args.pickupFSW):
                    if(args.orlogic):
                        dev.trig.leveltwo_logic = 1
                        for i in range(48): 
                            surf.levelone.write(0x800 + i*4,thresholdOR_BLITS) #
                        surf.levelone.write(0x1800, 2)# Apply new thresholds
                    else:
                        dev.trig.leveltwo_logic = 0
                        for i in range(48): 
                            surf.levelone.write(0x800 + i*4,thresholdAND_BLITS) #
                        surf.levelone.write(0x1800, 2)# Apply new thresholds
        else:
            for s in range(6): 
                surf = PueoSURF((tio, s), 'TURFIO')#6500
                if surf.trig_clock_en != 1 : 
                    print("Yo, the RF stuff ain't set up right")
                    sys.exit()
                if(not args.pickupFSW):
                    if(args.orlogic):
                        dev.trig.leveltwo_logic = 1
                        for i in range(48): 
                            surf.levelone.write(0x800 + i*4,thresholdOR_BLITS) #
                        surf.levelone.write(0x1800, 2)# Apply new thresholds 
                    else:
                        dev.trig.leveltwo_logic = 0
                        for i in range(48): 
                            surf.levelone.write(0x800 + i*4,thresholdAND_BLITS) #
                        surf.levelone.write(0x1800, 2)# Apply new thresholds 

    if(args.maskLF):
        dev.trig.mask = 0b110000000000000000000000000
    else:
        dev.trig.mask = 0b000000000000000000000000000

    if(not args.pickupFSW):
        dev.trig.mask = 0
        if(args.orlogic):
            dev.trig.leveltwo_logic = 1
        else:
            dev.trig.leveltwo_logic = 0
    else:
        print(f"Started with {dev.trig.mask} mask and {dev.trig.leveltwo_logic} L2 logic reg")

    es.open()
    dev.trig.runcmd(dev.trig.RUNCMD_RESET)
    #dev.evstatus()
    startCount = dev.trig.trigger_count
    start = time.time()
    L2_begin = dev.trig.scaler.leveltwos()
    last100 = L2_begin
    for i in range(args.stop):
        print(i)
        print(f"Trig count BLITZ:{dev.trig.trigger_count}")
        print(dev.trig.scaler.leveltwos())
        if(i % 100 == 99):
            print(f'Mid Run BLITZ L2: {dev.trig.scaler.leveltwos()}')
            print(f'Event number BLITZ {i}')
            print(f'Average rate so far BLITZ: {100.0/(time.time() - last100)}')
            last100 = time.time()
        e = es.event_receive()
        f = open(f'{args.filename}_{i}.pkl', 'wb')
        pickle.dump(e,f)
        f.close()
    endCount = dev.trig.trigger_count
    end = time.time()
    L2_end = dev.trig.scaler.leveltwos()

    if(args.maskLF):
        print("MASKING LF")
    if(args.orlogic):
        print("USING L1 (OR) LOGIC")
    else:
        print("USING L2 (AND) LOGIC")
    print(f"Time delta: {end-start} s")
    print(f"Measured Rate: {args.stop/(end-start)} Hz")
    print(f"Trig delta: {endCount - startCount}")
    print(f"L2_begin: {L2_begin}")
    print(f"L2_end: {L2_end}")

    for i in range(449):
        es.es.recv(1032)

    es.close()
    dev.trig.runcmd(dev.trig.RUNCMD_STOP)

    ## LUCAS EDIT HERE FOR THE THRESHOLDS
    thresholdOR_LAST = 8000
    thresholdAND_LAST = 2500


    for i in range(4):
        tio = PueoTURFIO((dev, i), 'TURFGTP')
        if i == 0 or i == 1: 
            for s in range(7):
                surf = PueoSURF((tio, s), 'TURFIO')#6500
                if surf.trig_clock_en != 1 : 
                    print("Yo, the RF stuff ain't set up right")
                    sys.exit()
                if(not args.pickupFSW):
                    if(args.orlogic):
                        dev.trig.leveltwo_logic = 1
                        for i in range(48): 
                            surf.levelone.write(0x800 + i*4,thresholdOR_BLITS) #
                        surf.levelone.write(0x1800, 2)# Apply new thresholds
                    else:
                        dev.trig.leveltwo_logic = 0
                        for i in range(48): 
                            surf.levelone.write(0x800 + i*4,thresholdAND_BLITS) #
                        surf.levelone.write(0x1800, 2)# Apply new thresholds
        else:
            for s in range(6): 
                surf = PueoSURF((tio, s), 'TURFIO')#6500
                if surf.trig_clock_en != 1 : 
                    print("Yo, the RF stuff ain't set up right")
                    sys.exit()
                if(not args.pickupFSW):
                    if(args.orlogic):
                        dev.trig.leveltwo_logic = 1
                        for i in range(48): 
                            surf.levelone.write(0x800 + i*4,thresholdOR_BLITS) #
                        surf.levelone.write(0x1800, 2)# Apply new thresholds 
                    else:
                        dev.trig.leveltwo_logic = 0
                        for i in range(48): 
                            surf.levelone.write(0x800 + i*4,thresholdAND_BLITS) #
                        surf.levelone.write(0x1800, 2)# Apply new thresholds 

    if(args.maskLF):
        dev.trig.mask = 0b110000000000000000000000000
    else:
        dev.trig.mask = 0b000000000000000000000000000

    if(not args.pickupFSW):
        dev.trig.mask = 0
        if(args.orlogic):
            dev.trig.leveltwo_logic = 1
        else:
            dev.trig.leveltwo_logic = 0
    else:
        print(f"Started with {dev.trig.mask} mask and {dev.trig.leveltwo_logic} L2 logic reg")

    es.open()
    dev.trig.runcmd(dev.trig.RUNCMD_RESET)
    #dev.evstatus()
    startCount = dev.trig.trigger_count
    start = time.time()
    L2_begin = dev.trig.scaler.leveltwos()
    last100 = L2_begin
    for i in range(args.stop):
        print(i)
        print(f"Trig count LAST:{dev.trig.trigger_count}")
        print(dev.trig.scaler.leveltwos())
        if(i % 100 == 99):
            print(f'Mid Run LAST L2: {dev.trig.scaler.leveltwos()}')
            print(f'Event number LAST {i}')
            print(f'Average rate so far LAST: {100.0/(time.time() - last100)}')
            last100 = time.time()
        e = es.event_receive()
        f = open(f'{args.filename}_{i}.pkl', 'wb')
        pickle.dump(e,f)
        f.close()
    endCount = dev.trig.trigger_count
    end = time.time()
    L2_end = dev.trig.scaler.leveltwos()

    if(args.maskLF):
        print("MASKING LF")
    if(args.orlogic):
        print("USING L1 (OR) LOGIC")
    else:
        print("USING L2 (AND) LOGIC")
    print(f"Time delta: {end-start} s")
    print(f"Measured Rate: {args.stop/(end-start)} Hz")
    print(f"Trig delta: {endCount - startCount}")
    print(f"L2_begin: {L2_begin}")
    print(f"L2_end: {L2_end}")

    for i in range(449):
        es.es.recv(1032)

    es.close()
    dev.trig.runcmd(dev.trig.RUNCMD_STOP)
