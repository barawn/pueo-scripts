#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from EventTester import EventServer
import time
import numpy as np
import itertools

parser = argparse.ArgumentParser()

parser.add_argument("--tio", type=int)
parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")
parser.add_argument("--nbeams", type=int, default=48)
parser.add_argument("--smallThresh", type=int, default=2000)
parser.add_argument("--bigThresh", type=int, default=80000)
parser.add_argument("--avg", type=int, default=1)
parser.add_argument("--filename", default = "L2_permutation_scan.csv")

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))

dev = PueoTURF(None, 'Ethernet')

tio = PueoTURFIO((dev, args.tio), 'TURFGTP')

surfs = {}
for slot in slotList: 
    surfs[slot] = PueoSURF((tio, slot), 'TURFIO')

slot_combos = list(itertools.combinations(slotList,2))
beam_combos = list(itertools.permutations([i for i in range(args.nbeams)],2))
nbeams = args.nbeams
smallThresh = args.smallThresh
bigThresh = args.bigThresh
with open(args.filename, "w") as outfile:
    outfile.write("tio, slot, threshold, scaler\n")
    for slot_combo in slot_combos:
        print(f"-----SLOT {slot_combo[0]} and SLOT {slot_combo[1]}-----")
        surf0 = surfs[slot_combo[0]]
        surf1 = surfs[slot_combo[1]]
        surf0.levelone.write(0x2008,0x00000)#0xFFFFC)
        surf0.levelone.write(0x200c,0x80000000)#0x8FFFFFFF)
        print(f"SURF0: Masks are {surf0.levelone.read(0x2008):X} and {surf0.levelone.read(0x200C):X}")
        surf1.levelone.write(0x2008,0x00000)#0xFFFFC)
        surf1.levelone.write(0x200c,0x80000000)#0x8FFFFFFF)
        print(f"SURF1: Masks are {surf1.levelone.read(0x2008):X} and {surf1.levelone.read(0x200C):X}")
        for beam_combo in beam_combos:
            # SURF 0
            for idx in range(nbeams):
                if(beam_combo[0] == idx):
                    surf0.levelone.write(0x800 + idx*4, smallThresh)
                else:
                    surf0.levelone.write(0x800 + idx*4, bigThresh)
            for idx in range(nbeams):
                if(beam_combo[0] == idx):
                    surf0.levelone.write(0xA00 + idx*4, smallThresh)
                else:
                    surf0.levelone.write(0xA00 + idx*4, bigThresh)
            surf0.levelone.write(0x1800, 2)# Apply new thresholds 
            # SURF 1
            for idx in range(nbeams):
                if(beam_combo[1] == idx):
                    surf1.levelone.write(0x800 + idx*4, smallThresh)
                else:
                    surf1.levelone.write(0x800 + idx*4, bigThresh)
            for idx in range(nbeams):
                if(beam_combo[1] == idx):
                    surf1.levelone.write(0xA00 + idx*4, smallThresh)
                else:
                    surf1.levelone.write(0xA00 + idx*4, bigThresh)
            surf1.levelone.write(0x1800, 2)# Apply new thresholds 


            time.sleep(0.1)
            if(surf0.levelone.read(0x1800)):
                raise Exception(f'Threshold update.... failed?')
            time.sleep(0.1)
            if(surf1.levelone.read(0x1800)):
                raise Exception(f'Threshold update.... failed?')
            cols = len(dev.trig.scaler.leveltwos())
            trig_values0 = []
            trig_values1 = []
            l2_values = np.zeros((args.avg, cols))
            beam_values0 = {}
            beam_values1 = {}
            for i in range(args.avg):
                time.sleep(1)
                toggle0 = surf0.levelone.read(0x1804)
                toggle1 = surf1.levelone.read(0x1804)
                time.sleep(0.1)
                while(surf0.levelone.read(0x1804) == toggle0 or surf1.levelone.read(0x1804) == toggle1):
                    time.sleep(0.1)
                for idx in range(nbeams):
                    if(not idx in beam_values0.keys()):
                        beam_values0[idx] = []
                    rate0=surf0.levelone.read(0x400+4*idx)
                    trigger_rate0 = rate0 & 0x0000FFFF
                    subthreshold_rate0 = (rate0 & 0xFFFF0000) >> 16
                    beam_values0[idx].append(trigger_rate0)
                    if(not idx in beam_values1.keys()):
                        beam_values1[idx] = []
                    rate1=surf1.levelone.read(0x400+4*idx)
                    trigger_rate1 = rate1 & 0x0000FFFF
                    subthreshold_rate1 = (rate1 & 0xFFFF0000) >> 16
                    beam_values1[idx].append(trigger_rate1)
                trig_values0.append(dev.trig.scaler.read((0+slot_combo[0])* 4))# Slot 5 # was 28
                trig_values1.append(dev.trig.scaler.read((0+slot_combo[1])* 4))# Slot 5 # was 28
                l2_values[i] = np.array(dev.trig.scaler.leveltwos())
            for idx in range(nbeams):
                beam_avg0 = float(sum(beam_values0[idx]))/float(len(beam_values0[idx]))
                outfile.write(f"beam, {beam_combo[0]}, {beam_combo[1]}, {args.tio}, {slot_combo[0]}, {idx}, {beam_avg0:6f}\n")
                beam_avg1 = float(sum(beam_values1[idx]))/float(len(beam_values1[idx]))
                outfile.write(f"beam, {beam_combo[0]}, {beam_combo[1]}, {args.tio}, {slot_combo[1]}, {idx}, {beam_avg1:6f}\n")
            trig_avg0=sum(trig_values0)/float(len(trig_values0))
            trig_avg1=sum(trig_values1)/float(len(trig_values1))
            l2_avgs = np.mean(l2_values,axis=0)
            for idx in range(len(l2_avgs)):
                outfile.write(f"l2, {beam_combo[0]}, {beam_combo[1]}, {args.tio}, {slot_combo[0]}, {slot_combo[1]}, {idx}, {l2_avgs[idx]:6f}\n")
               # print(f"\tl2, {beam_combo[0]}, {beam_combo[1]}, {args.tio}, {slot_combo[0]}, {slot_combo[1]}, {idx}, {l2_avgs[idx]:6f}")
            print(f"L2: BEAM 0: {beam_combo[0]}\tBEAM 1:{beam_combo[1]}\t{l2_avgs}")
            outfile.write(f"trig, {args.tio}, {slot_combo[0]}, {trig_avg0}\n")
            outfile.write(f"trig, {args.tio}, {slot_combo[1]}, {trig_avg1}\n")
            #print(f"\nTIO:{args.tio:2d}, SLOT:{slot:2d}, THRESHOLD:{threshold_value:10d}, FULL_SCALER:{trig_avg:6f}")
    print("\n\n**********************")
