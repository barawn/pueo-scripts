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
if(len(coeffs) != 31):
    raise Exception("Wrong number of coefficients in coefficient file")
    
for slot in slotList: 
    surf = PueoSURF((tio, slot), 'TURFIO')
    for channel_idx in range(8):
        bq_offset = 0x6000
        bq_idx_offset = 0x80 * args.bq
        channel_idx_offset = 0x400 * channel_idx
        total_offset = bq_offset + bq_idx_offset + channel_idx_offset
        
        surf.levelone.write(total_offset + 0x04, coeffs[0]) #B
        surf.levelone.write(total_offset + 0x04, coeffs[1]) #A

        
        surf.levelone.write(total_offset + 0x08, coeffs[2]) #C2
        surf.levelone.write(total_offset + 0x08, coeffs[3]) #C3 (correct order)
        surf.levelone.write(total_offset + 0x08, coeffs[4]) #C1
        surf.levelone.write(total_offset + 0x08, coeffs[5]) #C0

        
        surf.levelone.write(total_offset + 0x0C, coeffs[6]) #a1'
        surf.levelone.write(total_offset + 0x0C, coeffs[7]) #a2'
        
        surf.levelone.write(total_offset + 0x10, coeffs[8]) #D_FF
        surf.levelone.write(total_offset + 0x10, coeffs[9]) #X_6
        surf.levelone.write(total_offset + 0x10, coeffs[10]) #X_5
        surf.levelone.write(total_offset + 0x10, coeffs[11]) #X_4
        surf.levelone.write(total_offset + 0x10, coeffs[12]) #X_3
        surf.levelone.write(total_offset + 0x10, coeffs[13]) #X_2
        surf.levelone.write(total_offset + 0x10, coeffs[14]) #X_1

        
        surf.levelone.write(total_offset + 0x14, coeffs[15]) #E_GG
        surf.levelone.write(total_offset + 0x14, coeffs[16]) #X_7
        surf.levelone.write(total_offset + 0x14, coeffs[17]) #X_6
        surf.levelone.write(total_offset + 0x14, coeffs[18]) #X_5
        surf.levelone.write(total_offset + 0x14, coeffs[19]) #X_4
        surf.levelone.write(total_offset + 0x14, coeffs[20]) #X_3
        surf.levelone.write(total_offset + 0x14, coeffs[21]) #X_2
        surf.levelone.write(total_offset + 0x14, coeffs[22]) #X_1

        
        surf.levelone.write(total_offset + 0x18, coeffs[23]) #D_FG
        
        surf.levelone.write(total_offset + 0x1C, coeffs[24]) #E_GF

        surf.levelone.write(total_offset, 1) #Update
        
    
