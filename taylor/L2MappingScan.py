from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
import time
import csv


filename = 'hello.csv'

highthreshold = 1200
highsub = 1000

lowthreshold = 800
lowsub = 200

headers = ['tio', 'slot0', 'slot1', 'slot2', 'slot3', 'slot4', 'slot5','tio0slot0', 'tio0slot1', 
           'tio0slot2', 'tio0slot3', 'tio0slot4', 'tio0slot5', 'LF',
           'AH','tio1slot0', 'tio1slot1', 'tio1slot2', 'tio1slot3', 'tio1slot4', 
           'tio1slot5','LF','NA','tio2slot0', 'tio2slot1', 'tio2slot2', 'tio2slot3', 'tio2slot4', 'tio2slot5',
           'NA','NA', 'tio3slot0', 'tio3slot1', 'tio3slot2', 'tio3slot3', 'tio3slot4', 'tio3slot5', 'NA','NA', 'HPol0', 
           'HPol1','HPol2','HPol3','HPol4','HPol5','HPol6','HPol7','HPol8','HPol9','HPol10','HPol11','VPol0',
           'VPol1','VPol2','VPol3','VPol4','VPol5','VPol6','VPol7','VPol8','VPol9','VPol10','VPol11']

dev = PueoTURF(None, 'Ethernet')

def thresholds(surf,threshold,subthreshold): 
    for i in range(48): 
        surf.levelone.write(0x800 + i*4, threshold) #
        surf.levelone.write(0xA00 + i*4, subthreshold) #
        surf.levelone.write(0x1800, 2)# Apply new thresholds 
        time.sleep(0.1)

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

def surfThresholdSet(surf0, surf1): 
    thresholds(surf0, lowthreshold, lowsub)
    thresholds(surf1, lowthreshold, lowsub)
    time.sleep(5)
    L2trigs = dev.trig.scaler.leveltwos()
    L1trigs = dev.trig.scaler.scalers()
    vals = thresholdCheck(dev)
    thresholds(surf0, highthreshold, highsub)
    return L1trigs, L2trigs, vals


"""
The mapping goes 

L2   :  0  1  2  3  4  5
TIO 0:  5  4  3  2  1  0 

L2   :  6  7  8  9  10  11
TIO 1:  0  1  2  3  4   5 

L2   :  12  13  14  15  16  17
TIO 3:  5   4   3   2   1   0 

L2   :  18  19  20  21  22  23
TIO 2:  0   1   2   3   4   5

"""
with open(filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    for t in range(4):
        tio = PueoTURFIO((dev,t), 'TURFGTP')
        if t == 0: 
            for s in range(5,-1,-1): 
                surf0 = PueoSURF((tio, s), 'TURFIO')
                if s != 0: 
                    surf1 = PueoSURF((tio, s+1), 'TURFIO')
                else: # if its the last SURF in the RACK, goes to next tio
                    surf1 = PueoSURF((1, 0), 'TURFIO')
                L1trigs, L2trigs, vals = surfThresholdSet(surf0,surf1)
                new_data = [t, *vals, *L1trigs, *L2trigs]
                csv_writer.writerow(new_data)
        elif t == 1: 
            for s in range(0,6): 
                surf0 = PueoSURF((tio, s), 'TURFIO')
                thresholds(surf0, lowthreshold, lowsub)
                if s != 5: 
                    surf1 = PueoSURF((tio, s+1), 'TURFIO')
                else: # if its the last SURF in the RACK, goes to previous tio
                    surf1 = PueoSURF((0, 0), 'TURFIO')
                L1trigs, L2trigs, vals = surfThresholdSet(surf0,surf1)
                new_data = [t, *vals, *L1trigs, *L2trigs]
                csv_writer.writerow(new_data)
        elif t+1 == 3: 
            for s in range(0,6): 
                surf0 = PueoSURF((tio, s), 'TURFIO')
                thresholds(surf0, lowthreshold, lowsub)
                if s != 5: 
                    surf1 = PueoSURF((tio, s+1), 'TURFIO')
                else: # if its the last SURF in the RACK, goes to previous tio
                    surf1 = PueoSURF((3, 0), 'TURFIO')
                L1trigs, L2trigs, vals = surfThresholdSet(surf0,surf1)
                new_data = [t, *vals, *L1trigs, *L2trigs]
                csv_writer.writerow(new_data)
        else: 
            for s in range(5,-1,-1): 
                surf0 = PueoSURF((tio, s), 'TURFIO')
                if s != 0: 
                    surf1 = PueoSURF((tio, s+1), 'TURFIO')
                else: # if its the last SURF in the RACK, goes to next tio
                    surf1 = PueoSURF((2, 5), 'TURFIO')
                L1trigs, L2trigs, vals = surfThresholdSet(surf0,surf1)
                new_data = [t, *vals, *L1trigs, *L2trigs]
                csv_writer.writerow(new_data)