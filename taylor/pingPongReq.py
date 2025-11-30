
"""from HskSerial import HskEthernet, HskPacket
import time
"""
# Stolen from Cosmin!!! 
#! /usr/bin/env python3

import time
import psycopg2
import sys
import os
import signal
import argparse

from HskSerial import HskEthernet, HskPacket

hsk = HskEthernet()

five_oclock = False
def on_timeout(signum,frame):
    raise TimeoutError()

def on_int(signum, frame):
    global five_oclock
    print ("Caught sigint")
    five_oclock = True

signal.signal(signal.SIGALRM, on_timeout)
signal.signal(signal.SIGINT, on_int)

def hsk_harder(dest, cmd, data = None, timeout = 1, max_tries = 5):
    pkt = None
    ntimeout = 0
#    time.sleep(0.1)
    global five_oclock
    while pkt is None and not five_oclock:
        hsk.send(HskPacket(dest, cmd, data))
        try:
            signal.alarm(timeout)
            pkt = hsk.receive()
            if pkt is None:
                print("WTF: %d %d\n" %( dest, cmd))
            signal.alarm(0)
        except: 
            ntimeout+=1
            if ntimeout == max_tries:
                print( "Giving up on " + str((dest,cmd)) + " after %d attempts " % (max_tries))
                return None
            print( str((dest,cmd)) + " timed out %d times trying again" % ( ntimeout))
            pkt = None


    return pkt


parser = argparse.ArgumentParser()
parser.add_argument("--tio", type=str, default="0,1,2,3", 
        help="comma-separated list of TURFIOs to initialize")
parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")

args = parser.parse_args()

slotList = list(map(int,args.slots.split(',')))

if args.tio == '0':
    tios = (0, 0x58)
    surfs = [ (0, 0x97),
            (1, 0xa0),
            (2, 0x99),
            (3, 0x8d),
            (4, 0x9d),
            (5, 0x94),
            (6, 0x8a) ]
elif args.tio == '1':
    tios = (1, 0x50)
    surfs = [ (0, 0x8c),
            (1, 0x95),
            (2, 0x9f),
            (3, 0x9a),
            (4, 0x87),
            (5, 0x85), 
            (6, 0x91)]
elif args.tio == '2':
    tios = (2, 0x40)
    surfs = [ (0, 0x89),
            (1, 0x88),
            (2, 0x9e),
            (3, 0x8b),
            (4, 0xa1),
            (5, 0x98)]
elif args.tio == '3':
    tios = (3, 0x48)
    surfs = [ (0, 0x93),
            (1, 0x9b),
            (2, 0x86),
            (3, 0x8e),
            (4, 0x90),
            (5, 0x92) ]
elif args.tio == 't':
    tios = (3, 0x48)
    surfs = [ (0, 0x93) ]



hsk = HskEthernet()

for s in slotList:    
    val = (surfs[s][1])
    if hsk_harder(val, 'ePingPong', max_tries=1) is None:
        hsk.send(HskPacket(tios[1], 'eEnable', data=[0x40, 0x40]))
        pkt = hsk.receive()
    if hsk_harder(val, 'ePingPong') is None:
        print(f"SURF SLOT#{surfs[s][0]} on TURFIO PORT#{tios[1]} failed to respond!")
        sys.exit()

print('All SURFs booted and ready')
    
            
   
