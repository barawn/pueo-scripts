#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from EventTester import EventServer
import time


parser = argparse.ArgumentParser()

parser.add_argument("--tio", type=int)
parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")
#parser.add_argument("--nbeams", type=int, default=2)
parser.add_argument("--min", type=int, default=50000)
parser.add_argument("--max", type=int, default=120000)
parser.add_argument("--step", type=int, default=1000)
parser.add_argument("--avg", type=int, default=2)
parser.add_argument("--filename", default = "thresh_scan.csv")


args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))


dev = PueoTURF(None, 'Ethernet')

tio = PueoTURFIO((dev, args.tio), 'TURFGTP')

surfs = {}
for slot in slotList: 
    surfs[slot] = PueoSURF((tio, slot), 'TURFIO')

nbeams = 48 #args.nbeams #(Fix masking if this becomes an arugment again)
    
with open(args.filename, "w") as outfile:
    outfile.write("tio, slot, threshold, scaler\n")
    for threshold_value in range(args.min, args.max, args.step):
        for slot in slotList:
            print(f"-----SLOT {slot}-----")
            surf = surfs[slot]
            surf.levelone.write(0x2008,0x00000)#0xFFFFC)
            surf.levelone.write(0x200c,0x80000000)#0x8FFFFFFF)
            print(f"Masks are {surf.levelone.read(0x2008):X} and {surf.levelone.read(0x200C):X}")
            if(threshold_value>0):
                for idx in range(nbeams): 
                    surf.levelone.write(0x800 + idx*4, threshold_value)
            if(threshold_value>0):
                for idx in range(nbeams):  
                    surf.levelone.write(0xA00 + idx*4, threshold_value) #
            surf.levelone.write(0x1800, 2)# Apply new thresholds 
            time.sleep(0.1)
            if(surf.levelone.read(0x1800)):
                raise Exception(f'Threshold update.... failed?')
            #print(f"Scanned {threshold_value} on {nbeams} beams")
            for i in range(args.avg):
                time.sleep(1)
                toggle = surf.levelone.read(0x1804)
                time.sleep(0.1)
                while(surf.levelone.read(0x1804) == toggle):
                    time.sleep(0.1)
                beam_values = {}
                for idx in range(nbeams):
                    if(not idx in beam_values.keys()):
                        beam_values[idx] = []
                    rate=surf.levelone.read(0x400+4*idx)
                    trigger_rate = rate & 0x0000FFFF
                    subthreshold_rate = (rate & 0xFFFF0000) >> 16
                    beam_values[idx].append(trigger_rate)
            for idx in range(nbeams):
                beam_avg = float(sum(beam_values[idx]))/float(len(beam_values[idx]))
                outfile.write(f"beam, {args.tio}, {slot}, {idx}, {threshold_value}, {beam_avg}\n")
                print(f"TIO:{args.tio:2d}, SLOT:{slot:2d}, BEAM:{idx:2f}, THRESH:{threshold_value:6d}, SCALER:{beam_avg:6f}")

            trig_values = []
            for i in range(args.avg):
                time.sleep(2) # time to accumulate
                #trig_values.append(dev.trig.scaler.read((24+slot)* 4))# Slot 5 # was 28
                # for spare
                trig_values.append(dev.trig.scaler.read((0+slot)* 4))# Slot 5 # was 28
            trig_avg=sum(trig_values)/float(len(trig_values))
            outfile.write(f"trig, {args.tio}, {slot}, {threshold_value}, {trig_avg}\n")
            print(f"\nTIO:{args.tio:2d}, SLOT:{slot:2d}, THRESHOLD:{threshold_value:10d}, FULL_SCALER:{trig_avg:6f}\n")
        print("\n\n**********************")
