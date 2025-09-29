
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
import csv 

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


tio0 = (0, 0x58)
surf0 = [ (0, 0x97),
        (1, 0xa0),
        (2, 0x99),
        (3, 0x8d),
        (4, 0x9d),
        (5, 0x94),
        (6, 0x8a) ]

tio1 = (1, 0x50)
surf1 = [ (0, 0x8c),
        (1, 0x95),
        (2, 0x9f),
        (3, 0x9a),
        (4, 0x87),
        (5, 0x85), 
        (6, 0x91)]

tio2 = (2, 0x40)
surf2 = [ (0, 0x89),
        (1, 0x88),
        (2, 0x9e),
        (3, 0x8b),
        (4, 0xa1),
        (5, 0x98)]

tio3 = (3, 0x48)
surf3 = [ (0, 0x93),
        (1, 0x9b),
        (2, 0x86),
        (3, 0x8e),
        (4, 0x90),
        (5, 0x92) ]

tios = [tio0, tio1, tio2, tio3]
surfs = [surf0, surf1, surf2, surf3]


for i in range(0,4): 
    tio = tios[i][1]
    surf = surfs[i]
    
    for j in range(len(surf)):
        val = (surf[j][1])
        if hsk_harder(val, 'ePingPong', max_tries=1) is None:
            hsk.send(HskPacket(tio, 'eEnable', data=[0x40, 0x40]))
            pkt = hsk.receive()
        hsk.send(HskPacket(tio, 'eTemps'))
        pkt = hsk.receive().data 
        tfiotemp = int.from_bytes(pkt[0:2])
        srftemp = []
        for iter in range(2,16,2): 
            srftemp.append(int.from_bytes(pkt[iter:iter+2]))

        temparray = []
        tfiotemp = ((tfiotemp * 503.975) / 2 ** 12) -273.15
        temparray.append(tfiotemp)
        
            
        for iter in range(len(srftemp)): 
            if srftemp[iter] != 0: 
                srftemp[iter] = format((( srftemp[iter] * 10 - 31880) / 42), '.2f')
                temparray.append(srftemp[iter])
                
            else:
                temparray.append('NaN')
        with open('why.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(temparray)
        
"""

print('All SURFs booted and ready')


print("")
        pkttf = self.packetsend(self.TF, 'eTemps')
        tftemp = self.tempTURFIO(pkttf) # just in case


        rpuTemps = []
        apuTemps = []
        for iter in range(0, self.endVal):
            
            pktsf = self.packetsend(self.SF[iter], 'eTemps' )
            rpuTemp, apuTemp = self.tempSURF(pktsf, self.SF[iter])
            rpuTemps.append(rpuTemp)
            apuTemps.append(apuTemp)

        print("TURFIO: {}C".format(format(tftemp[0], '.2f')))
        print("")
        for iter in range(0, self.endVal): 
            print('SURF {}'.format(self.hextodec(self.SF[iter])))
            print('Hotswap: {}C'.format(tftemp[iter+1]))
            print("RPU: {}C".format(format(rpuTemps[iter], '.2f')))
            print("APU: {}C".format(format(apuTemps[iter], '.2f')))
            print("")
    """