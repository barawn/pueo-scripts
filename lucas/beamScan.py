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

parser.add_argument("--tio", type=int, default=0)
parser.add_argument("--slots", type=str, default="6")

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))

dev = PueoTURF(None, 'Ethernet')

tio = PueoTURFIO((dev, args.tio), 'TURFGTP')

def scaler_monitor(dev, period=1, n=10):
    for i in range(n):
        time.sleep(period)
        print(f"Scaler reads {dev.trig.scaler.scaler(4*slot)}")    


with open("beamScan.csv","w") as f:
    for slot in slotList: 
        surf = PueoSURF((tio, slot), 'TURFIO')
        
        # UNMASK ALL
        surf.levelone.write(0x2008,0x00000000)
        surf.levelone.write(0x200c,0x80000000)
        time.sleep(0.5)
        surf.levelone.write(0x2008,0x00000000)
        surf.levelone.write(0x200c,0x80000000)

        for beam_on in range(48):            
            for beam_idx in range(48):
                if(beam_on == beam_idx):
                    surf.levelone.write(0x800 + beam_idx*4, 7000)
                else:
                    surf.levelone.write(0x800 + beam_idx*4, 7000+80000)
            surf.levelone.write(0x1800, 2)# Apply new thresholds 
            time.sleep(2)
            for beam_idx in range(48):
                rate=surf.levelone.read(0x400+4*beam_idx)
                trigger_rate = rate & 0x0000FFFF
                subthreshold_rate = (rate & 0xFFFF0000) >> 16
                f.write(f"{slot}, {beam_on}, {beam_idx}, {trigger_rate}\n")    
                print(f"{slot}, {beam_on}, {beam_idx}, {trigger_rate}")
            f.write(f"{slot}, {beam_on}, -1, {dev.trig.scaler.scaler(4*slot)}\n")    
            print(f"{slot}, {beam_on}, -1, {dev.trig.scaler.scaler(4*slot)}")
