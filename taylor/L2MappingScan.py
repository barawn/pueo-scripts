from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from EventTester import EventServer
import time
import csv


filename = 'thresholdScanL2take2.csv'

highthreshold = 17000
highsub = 10000

lowthreshold = 5000
lowsub = 1000

headers = ['tio', 'thr t0 s0', 'thr t0 s1', 'thr t0 s2', 'thr t0 s3', 'thr t0 s4', 'thr t0 s5', 'thr t0 s6', 
           'thr t1 s0','thr t1 s1','thr t1 s2','thr t1 s3','thr t1 s4','thr t1 s5','thr t1 s6',
           'thr t2 s0','thr t2 s1','thr t2 s2','thr t2 s3','thr t2 s4','thr t2 s5','thr t2 s6',
           'thr t3 s0','thr t3 s1','thr t3 s2','thr t3 s3','thr t3 s4','thr t3 s5','thr t3 s6',
           'L1 t0 s0', 'L1 t0 s1', 'L1 t0 s2', 'L1 t0 s3', 'L1 t0 s4', 'L1 t0 s5', 'LF',
           'NA','L1 t1 s0', 'L1 t1 s1', 'L1 t1 s2', 'L1 t1 s3', 'L1 t1 s4', 
           'L1 t1 s5','LF','NA','L1 t2 s0', 'L1 t2 s1', 'L1 t2 s2', 'L1 t2 s3', 'L1 t2 s4', 'L1 t2 s5',
           'NA','NA', 'L1 t3 s0', 'L1 t3 s1', 'L1 t3 s2', 'L1 t3 s3', 'L1 t3 s4', 'L1 t3 s5', 'NA','NA', 'HPol0', 
           'HPol1','HPol2','HPol3','HPol4','HPol5','HPol6','HPol7','HPol8','HPol9','HPol10','HPol11','VPol0',
           'VPol1','VPol2','VPol3','VPol4','VPol5','VPol6','VPol7','VPol8','VPol9','VPol10','VPol11']

dev = PueoTURF(None, 'Ethernet')
dev.trig.rf_trig_en = 0 
es = EventServer()
es.open()
dev.trig.runcmd(dev.trig.RUNCMD_RESET)
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

def surfThresholdSet(surf0, surf1,lowthreshold,lowsub,highthreshold,highsub): 
    thresholds(surf0, lowthreshold, lowsub)
    thresholds(surf1, lowthreshold, lowsub)
    time.sleep(5)
    L2trigs = dev.trig.scaler.leveltwos()
    L1trigs = dev.trig.scaler.scalers()
    vals = thresholdCheck(dev)
    thresholds(surf0, highthreshold, highsub)
    time.sleep(3)
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

# start off with everything high
for t in range(4):
    tio = PueoTURFIO((dev,t), 'TURFGTP')
    for s in range(0,7): 
        surf = PueoSURF((tio, s), 'TURFIO')
        thresholds(surf,highthreshold,highsub)
        time.sleep(5)


with open(filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(headers)
    for t in range(4):
        tio = PueoTURFIO((dev,t), 'TURFGTP')
        if t == 0: 
            for s in range(5,-1,-1): # 
                surf0 = PueoSURF((tio, s), 'TURFIO')
                if s != 0: 
                    surf1 = PueoSURF((tio, s-1), 'TURFIO')
                else: # if its the last SURF in the RACK, goes to next tio
                    tio1 = PueoTURFIO((dev, 1), 'TURFGTP') 
                    surf1 = PueoSURF((tio1, 0), 'TURFIO')
                L1trigs, L2trigs, vals = surfThresholdSet(surf0,surf1,lowthreshold,lowsub,highthreshold,highsub)
                new_data = [t, *vals, *L1trigs, *L2trigs]
                csv_writer.writerow(new_data)
        elif t == 1: 
            for s in range(0,6): 
                surf0 = PueoSURF((tio, s), 'TURFIO')
                thresholds(surf0, lowthreshold, lowsub)
                if s != 5: 
                    surf1 = PueoSURF((tio, s+1), 'TURFIO')
                else: # if its the last SURF in the RACK, goes to previous tio
                    tio1 = PueoTURFIO((dev, 0), 'TURFGTP') 
                    surf1 = PueoSURF((tio1, 5), 'TURFIO')
                L1trigs, L2trigs, vals = surfThresholdSet(surf0,surf1,lowthreshold,lowsub,highthreshold,highsub)
                new_data = [t, *vals, *L1trigs, *L2trigs]
                csv_writer.writerow(new_data)
            thresholds(surf1,highthreshold,highsub)
            thresholds(surf0,highthreshold,highsub)
        elif t+1 == 3:
            tio = PueoTURFIO((dev,t+1), 'TURFGTP') 
            for s in range(5,-1,-1): 
                surf0 = PueoSURF((tio, s), 'TURFIO')
                if s != 0: 
                    surf1 = PueoSURF((tio, s-1), 'TURFIO')
                else: # if its the last SURF in the RACK, goes to next tio
                    tio1 = PueoTURFIO((dev,2), 'TURFGTP') 
                    surf1 = PueoSURF((tio1, 5), 'TURFIO')
                L1trigs, L2trigs, vals = surfThresholdSet(surf0,surf1,lowthreshold,lowsub,highthreshold,highsub)
                new_data = [t, *vals, *L1trigs, *L2trigs]
                csv_writer.writerow(new_data)
            else:    
                tio = PueoTURFIO((dev,2), 'TURFGTP') 
                for s in range(0,6): 
                    surf0 = PueoSURF((tio, s), 'TURFIO')
                    thresholds(surf0, lowthreshold, lowsub)
                    if s != 5: 
                        surf1 = PueoSURF((tio, s+1), 'TURFIO')
                    else: # if its the last SURF in the RACK, goes to previous tio
                        tio1 = PueoTURFIO((dev,3), 'TURFGTP') 
                        surf1 = PueoSURF((tio1, 0), 'TURFIO')
                    L1trigs, L2trigs, vals = surfThresholdSet(surf0,surf1,lowthreshold,lowsub,highthreshold,highsub)
                    new_data = [t, *vals, *L1trigs, *L2trigs]
                    csv_writer.writerow(new_data)
                thresholds(surf1,highthreshold,highsub)
                thresholds(surf0,highthreshold,highsub)

es.close()
dev.trig.runcmd(dev.trig.RUNCMD_STOP) 
