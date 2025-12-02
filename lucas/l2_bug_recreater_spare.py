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
args = parser.parse_args()

dev = PueoTURF()
es = EventServer()

tio1 = PueoTURFIO((dev, 0), 'TURFGTP')
surf1 = PueoSURF((tio1, 3), 'TURFIO')#6500

if surf1.trig_clock_en != 1 : 
    print("Yo, the RF stuff ain't set up right")
    sys.exit(1) 

surf2 = PueoSURF((tio1, 4), 'TURFIO')#8900

if surf2.trig_clock_en != 1 : 
    print("Yo, the RF stuff ain't set up right")
    sys.exit(1) 

if(args.maskLF):
    dev.trig.mask = 0b110000000000000000000000000
else:
    dev.trig.mask = 0b000000000000000000000000000
    
if(args.orlogic):
    dev.trig.leveltwo_logic = 1
    for i in range(48): 
        surf1.levelone.write(0x800 + i*4,6700) #
    surf1.levelone.write(0x1800, 2)# Apply new thresholds 
    for i in range(48): 
        surf2.levelone.write(0x800 + i*4,9200) #
    surf2.levelone.write(0x1800, 2)# Apply new thresholds 
else:
    dev.trig.leveltwo_logic = 0
    for i in range(48): 
        surf1.levelone.write(0x800 + i*4,5500) #
    surf1.levelone.write(0x1800, 2)# Apply new thresholds 
    for i in range(48): 
        surf2.levelone.write(0x800 + i*4,5500) #
    surf2.levelone.write(0x1800, 2)# Apply new thresholds 

    
dev.event.mask = 0b1110
dev.trig.mask = 0
if(args.orlogic):
    dev.trig.leveltwo_logic = 1
else:
    dev.trig.leveltwo_logic = 0

es.open()
dev.trig.runcmd(dev.trig.RUNCMD_RESET)
#dev.evstatus()
startCount = dev.trig.trigger_count
start = time.time()
L2_begin = dev.trig.scaler.leveltwos()
for i in range(args.stop):
    if(i % 100 == 0):
        print(f'Mid Run L2: {dev.trig.scaler.leveltwos()}')
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
#dev.evstatus()
