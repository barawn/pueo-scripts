import argparse
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
import time
import csv


filename = 'hello.csv'

highthreshold = 1200
highsub = 1000

regularthreshold = 800
regsub = 200

headers = ['tio', 'slot0', 'slot1', 'slot2', 'slot3', 'slot4', 'slot5', 'slot6', 'tio0slot0', 'tio0slot1', 
           'tio0slot2', 'tio0slot3', 'tio0slot4', 'tio0slot5', 'LF',
           'AH','tio1slot0', 'tio1slot1', 'tio1slot2', 'tio1slot3', 'tio1slot4', 
           'tio1slot5','LF','NA','tio2slot0', 'tio2slot1', 'tio2slot2', 'tio2slot3', 'tio2slot4', 'tio2slot5',
           'NA','NA', 'tio3slot0', 'tio3slot1', 'tio3slot2', 'tio3slot3', 'tio3slot4', 'tio3slot5', 'NA','NA', 'HPol0', 
           'HPol1','HPol2','HPol3','HPol4','HPol5','HPol6','HPol7','HPol8','HPol9','HPol10','HPol11','VPol0',
           'VPol1','VPol2','VPol3','VPol4','VPol5','VPol6','VPol7','VPol8','VPol9','VPol10','VPol11']

dev = PueoTURF(None, 'Ethernet')

# Set thresholds.. stolen from thresholdsRFAll.py
def thresholds(surf,threshold,subthreshold): 
    for i in range(48): 
        surf.levelone.write(0x800 + i*4, threshold) #
        surf.levelone.write(0xA00 + i*4, subthreshold) #
    surf.levelone.write(0x1800, 2)# Apply new thresholds 

# I want a printout of every threshold in the game per run
# Proof that we are scanning across
def thresholdCheck(dev): 
    thresholdVals = []
    for t in range(4):
        tio = PueoTURFIO((dev, t), 'TURFGTP')
        if t == 0 or t == 1: 
            for s in range(7):
                surf = PueoSURF((tio, s), 'TURFIO')
                thresholdVals.append(surf.levelone.read(0x800))
        else: 
            for s in range(6):
                surf = PueoSURF((tio, s), 'TURFIO')
                thresholdVals.append(surf.levelone.read(0x800))
            thresholdVals.append(0)
    return thresholdVals



with open(filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    for t in range(4):
        tio = PueoTURFIO((dev,t), 'TURFGTP')
        if t == 0 or t == 1: 
            for s in range(7): 
                if s != 6:
                    surf0 = PueoSURF((tio, s), 'TURFIO')
                    thresholds(surf0, regularthreshold, regsub)
                    surf1 = PueoSURF((tio, s+1), 'TURFIO')
                    thresholds(surf1, regularthreshold, regsub)
                    time.sleep(5)
                    L1trigs = dev.trig.scaler.scalers()
                    trigs = dev.trig.scaler.leveltwos()
                    vals = thresholdCheck(dev)
                    thresholds(surf0, highthreshold, highsub)
                    new_data = [t, *vals, *L1trigs, *trigs]
                    csv_writer.writerow(new_data)
                else: 
                    surf0 = PueoSURF((tio, s), 'TURFIO')
                    thresholds(surf0, regularthreshold, regsub)
                    surf1 = PueoSURF((tio, 0), 'TURFIO')
                    thresholds(surf1, regularthreshold, regsub)
                    time.sleep(5)
                    L1trigs = dev.trig.scaler.scalers()
                    trigs = dev.trig.scaler.leveltwos()
                    vals = thresholdCheck(dev)
                    thresholds(surf0, highthreshold, highsub)
                    new_data = [t, *vals, *L1trigs, *trigs]
                    csv_writer.writerow(new_data)
        else:
            for s in range(6): 
                if s!= 5:
                    surf0 = PueoSURF((tio, s), 'TURFIO')
                    thresholds(surf0, regularthreshold, regsub)
                    surf1 = PueoSURF((tio, s+1), 'TURFIO')
                    thresholds(surf1, regularthreshold, regsub)
                    time.sleep(5)
                    trigs = dev.trig.scaler.leveltwos()
                    vals = thresholdCheck(dev)
                    _ = thresholds(surf0, highthreshold, highsub)
                    new_data = [t, s, *vals, *trigs]
                    csv_writer.writerow(new_data)
                else: 
                    surf0 = PueoSURF((tio, s), 'TURFIO')
                    thresholds(surf0, regularthreshold, regsub)
                    surf1 = PueoSURF((tio, 0), 'TURFIO')
                    thresholds(surf1, regularthreshold, regsub)
                    time.sleep(5)
                    trigs = dev.trig.scaler.leveltwos()
                    vals = thresholdCheck(dev)
                    _ = thresholds(surf0, highthreshold, highsub)
                    new_data = [t, s, *vals, *trigs]
                    csv_writer.writerow(new_data)
                

                