#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from EventTester import EventServer
import time
#import numpy as np

parser = argparse.ArgumentParser()

#parser.add_argument("--tio", type=int)
#parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")
#parser.add_argument("--nbeams", type=int, default=2)
parser.add_argument("--min", type=int, default=3000)
parser.add_argument("--max", type=int, default=25000)
parser.add_argument("--step", type=int, default=1000)
parser.add_argument("--avg", type=int, default=2)
#parser.add_argument("--l2", action="store_true")
parser.add_argument("--filename", default = "thresh_scan.csv")


args = parser.parse_args()

#slotList = list(map(int,args.slots.split(',')))


dev = PueoTURF(None, 'Ethernet')

#tio = PueoTURFIO((dev, args.tio), 'TURFGTP')

tios = []
tios.append(PueoTURFIO((dev, 0), 'TURFGTP'))
tios.append(PueoTURFIO((dev, 1), 'TURFGTP'))
tios.append(PueoTURFIO((dev, 2), 'TURFGTP'))
tios.append(PueoTURFIO((dev, 3), 'TURFGTP'))

surfs = {}

for tio_idx in range(4):
    surfs[tio_idx] = {}
    if tio_idx < 2:
        for slot_idx in range(7):
            print(f"({tio_idx},{slot_idx})")
            surfs[tio_idx][slot_idx] = PueoSURF((tios[tio_idx], slot_idx), 'TURFIO')
    else:
        for slot_idx in range(6):
            print(f"({tio_idx},{slot_idx})")
            surfs[tio_idx][slot_idx] = PueoSURF((tios[tio_idx], slot_idx), 'TURFIO')
            

nbeams = 48 #args.nbeams #(Fix masking if this becomes an arugment again)

with open(args.filename, "w") as outfile:
    outfile.write("First column is type\n")
    for threshold_value in range(args.min, args.max, args.step):
        for tio_idx in range(4):
            for slot_idx in range(len(surfs[tio_idx].keys())):
                print(f"-----SLOT {slot_idx}-----")
                surf = surfs[tio_idx][slot_idx]
                surf.levelone.write(0x2008,0x00000)#0xFFFFC)
                surf.levelone.write(0x200c,0x80000000)#0x8FFFFFFF)
                print(f"Masks are {surf.levelone.read(0x2008):X} and {surf.levelone.read(0x200C):X}")
                if(threshold_value>0):
                    for idx in range(nbeams): 
                        surf.levelone.write(0x800 + idx*4, threshold_value)
                if(threshold_value>0): # Subthreshold
                    for idx in range(nbeams):
                        surf.levelone.write(0xA00 + idx*4, threshold_value) #
                surf.levelone.write(0x1800, 2)# Apply new thresholds
        time.sleep(4)
        for i in range(args.avg):
            time.sleep(1.5)        
            for tio_idx in range(4):
                for slot_idx in range(len(surfs[tio_idx].keys())):
                    surf=surfs[tio_idx][slot_idx]
                    if(surf.levelone.read(0x1800)):
                        raise Exception(f'Threshold update.... failed?')
                    beam_values = {}
                    for idx in range(nbeams):
                        rate=surf.levelone.read(0x400+4*idx)
                        trigger_rate = rate & 0x0000FFFF
                        subthreshold_rate = (rate & 0xFFFF0000) >> 16
                        if(not idx in beam_values.keys()):
                            beam_values[idx] = trigger_rate
                        outfile.write(f"beam, {tio_idx}, {slot_idx}, {idx}, {threshold_value}, {trigger_rate:6f}\n")
                    trig_value = dev.trig.scaler.read((0+slot_idx)* 4)# Slot 5 # was 28
                    outfile.write(f"trig, {tio_idx}, {slot_idx}, {threshold_value}, {trig_value}\n")

                    print(f"\nTIO:{tio_idx:2d}, SLOT:{slot_idx:2d}, THRESHOLD:{threshold_value:10d}, LAST_FULL_SCALER:{trig_value:6f}")
                    for idx in range(nbeams):
                        print(f"\t{idx}: {beam_values[idx]}")

            l2_vals = dev.trig.scaler.leveltwos()
            print("----- L2 -----")
            for idx in range(len(l2_vals)):
                outfile.write(f"l2, {idx}, {threshold_value}, {l2_vals[idx]:6f}\n")
            print(f"l2, {threshold_value}, {l2_vals}")
            print("\n\n**********************")

                    
