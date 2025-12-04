#!/usr/bin/env python3

from HskSerial import HskEthernet, HskPacket
import argparse
import pickle
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from EventTester import EventServer
import time

def signed_to_uint32(value):
    """Convert a signed integer to its unsigned 32-bit two's-complement representation."""
    return value & 0xFFFFFFFF


parser = argparse.ArgumentParser()

parser.add_argument("--tio", type=int)
parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")
parser.add_argument("--coeffs", type=str, default="coeffs.dat")
parser.add_argument("--bq", type=int, default=0)
parser.add_argument("--bypass", action="store_true")
parser.add_argument("--BQOn", action="store_true")

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))


dev = PueoTURF(None, 'Ethernet')
tio = PueoTURFIO((dev, args.tio), 'TURFGTP')

coeffs = []
with open(args.coeffs, 'r') as coeff_file:
    for line in coeff_file:
        try:
            val = int(line)
        except Exception as e:
            continue
        coeffs.append(signed_to_uint32(val))
if(len(coeffs) != 23):
    print(len(coeffs))
    raise Exception("Wrong number of coefficients in coefficient file")

# Organize coefficients
B = signed_to_uint32(coeffs[0])
A = signed_to_uint32(coeffs[1])

C2 = signed_to_uint32(coeffs[2])
C3 = signed_to_uint32(coeffs[3])
C1 = signed_to_uint32(coeffs[4])
C0 = signed_to_uint32(coeffs[5])

a2 = signed_to_uint32(-1*coeffs[6]) # check negativity against testbench
a1 = signed_to_uint32(-1*coeffs[7])

DFF = signed_to_uint32(coeffs[8])
Fx2 = signed_to_uint32(coeffs[9])
Fx1 = signed_to_uint32(coeffs[10])

EGG = signed_to_uint32(coeffs[11])
Gx3 = signed_to_uint32(coeffs[12])
Gx2 = signed_to_uint32(coeffs[13])
Gx1 = signed_to_uint32(coeffs[14])

DFG = signed_to_uint32(coeffs[15])
EGF = signed_to_uint32(coeffs[16])

# [17]-[22] are the original coefficients in floating point


for slot in slotList:
    surf = PueoSURF((tio, slot), 'TURFIO')    
    for channel_idx in range(8):
        bq_offset = 0x6000
        bq_idx_offset = 0x80 * args.bq
        channel_idx_offset = 0x400 * channel_idx
        total_offset = bq_offset + bq_idx_offset + channel_idx_offset
        if(args.bypass):
            surf.levelone.write(total_offset + 0x0, 0x800000) # Enable Bypass
        elif(args.BQOn):
            # Yes they need to be sent in like this
            surf.levelone.write(total_offset + 0x04, B) #B
            surf.levelone.write(total_offset + 0x04, A) #A
            surf.levelone.write(total_offset + 0x04, B) #B
            surf.levelone.write(total_offset + 0x04, A) #A
            surf.levelone.write(total_offset + 0x04, B) #B
            surf.levelone.write(total_offset + 0x04, A) #A
            surf.levelone.write(total_offset + 0x04, B) #B
            surf.levelone.write(total_offset + 0x04, A) #A

            
            surf.levelone.write(total_offset + 0x10, DFF) # F Pipeline
            surf.levelone.write(total_offset + 0x10, Fx1) # X1
            surf.levelone.write(total_offset + 0x10, Fx2) # X2
            
            surf.levelone.write(total_offset + 0x14, EGG) # G Pipeline
            surf.levelone.write(total_offset + 0x14, Gx2) # X2
            surf.levelone.write(total_offset + 0x14, Gx3) # X3
            surf.levelone.write(total_offset + 0x14, Gx1) # X3

            surf.levelone.write(total_offset + 0x18, DFG) # F Cross
            surf.levelone.write(total_offset + 0x1C, EGF) # G Cross

            surf.levelone.write(total_offset + 0x08, C2) # C2
            surf.levelone.write(total_offset + 0x08, C3) # C3
            surf.levelone.write(total_offset + 0x08, C1) # C1
            surf.levelone.write(total_offset + 0x08, C0) # C0

            surf.levelone.write(total_offset + 0x0C, a1) # C1
            surf.levelone.write(total_offset + 0x0C, a2) # C0
            surf.levelone.write(total_offset + 0x0C, a1) # C1
            surf.levelone.write(total_offset + 0x0C, a2) # C0

            surf.levelone.write(total_offset + 0x00, 0x10001) #Update

            surf.levelone.write(total_offset + 0x0, 0x810000) # Enable Bypass
            print("BQ_ON")
        else:
            print("You didn't tell me on or off!")
            exit()


