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


with open("scaler_debug.txt","w") as f:
    for slot in slotList: 
        surf = PueoSURF((tio, slot), 'TURFIO')
        for beam_idx in range(48): 
            surf.levelone.write(0x800 + beam_idx*4, 7000)

        # UNMASK ALL
        surf.levelone.write(0x2008,0x00000000)
        surf.levelone.write(0x200c,0x80000000)
        time.sleep(0.5)
        surf.levelone.write(0x2008,0x00000000)
        surf.levelone.write(0x200c,0x80000000)
        surf.levelone.write(0x1800, 2)# Apply new thresholds 

        f.write("Unmasked all beams.\n")
        f.write(f"Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}\n")    
        time.sleep(5)
        scaler_monitor(dev)
        f.write(f"Scaler reads {dev.trig.scaler.scaler(4*slot)}\n")    

        f.write(f"Masking only lower mask\n")
        surf.levelone.write(0x2008,0xFFFFFFFF)
        f.write(f"Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}\n")    
        time.sleep(5)
        scaler_monitor(dev)
        f.write(f"Scaler reads {dev.trig.scaler.scaler(4*slot)}\n\n")    


        f.write(f"Masking upper mask, lower mask unchanged\n")
        surf.levelone.write(0x200c,0xFFFFFFFF)
        f.write(f"Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}\n")    
        time.sleep(5)
        scaler_monitor(dev)
        f.write(f"Scaler reads {dev.trig.scaler.scaler(4*slot)}\n\n")

        f.write(f"Masking lower mask (again), upper mask unchanged\n")
        surf.levelone.write(0x2008,0xFFFFFFFF)
        f.write(f"Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}\n")    
        time.sleep(5)
        scaler_monitor(dev)
        f.write(f"Scaler reads {dev.trig.scaler.scaler(4*slot)}\n\n")

        f.write(f"Masking upper mask (again), upper mask unchanged\n")
        surf.levelone.write(0x200c,0xFFFFFFFF)
        f.write(f"Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}\n")    
        time.sleep(5)
        scaler_monitor(dev)
        f.write(f"Scaler reads {dev.trig.scaler.scaler(4*slot)}\n\n")



        f.write(f"UNMasking only lower mask\n")
        surf.levelone.write(0x2008,0x80000000)
        f.write(f"Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}\n")    
        time.sleep(5)
        scaler_monitor(dev)
        f.write(f"Scaler reads {dev.trig.scaler.scaler(4*slot)}\n\n")    

        f.write(f"UNMasking upper mask, lower mask unchanged\n")
        surf.levelone.write(0x200c,0x80000000)
        f.write(f"Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}\n")    
        time.sleep(5)
        scaler_monitor(dev)
        f.write(f"Scaler reads {dev.trig.scaler.scaler(4*slot)}\n\n")

        f.write(f"UNMasking lower mask (again), upper mask unchanged\n")
        surf.levelone.write(0x2008,0x80000000)
        f.write(f"Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}\n")    
        time.sleep(5)
        scaler_monitor(dev)
        f.write(f"Scaler reads {dev.trig.scaler.scaler(4*slot)}\n\n")

        f.write(f"UNMasking upper mask (again), upper mask unchanged\n")
        surf.levelone.write(0x200c,0x80000000)
        f.write(f"Masks set to {surf.levelone.read(0x200c):08X} {surf.levelone.read(0x2008):08X}\n")    
        time.sleep(5)
        scaler_monitor(dev)
        f.write(f"Scaler reads {dev.trig.scaler.scaler(4*slot)}\n\n")

