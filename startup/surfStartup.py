from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
import time
import sys
import argparse
from itertools import chain

#
# This has gotten incredibly painful and likely needs to be cleaned up a ton.
# It starts up the SURFs and then aligns the return paths, which means
# aligning data inputs at the TURFIOs, then aligning the trigger inputs
# at the TURFIO and then at the TURF.
# 


parser = argparse.ArgumentParser()
parser.add_argument("--enable")
parser.add_argument("--cout")
args = parser.parse_args()

# WHATEVER JUST HARDCODE THIS FOR NOW
surfList = [ (0, 0), (0, 5) ]

dev = PueoTURF(None, 'Ethernet')
tio = {}
masks = {}
for surfAddr in surfList:
    if surfAddr[0] not in tio:
        print(f'Building TURFIO#{surfAddr[0]}')
        tio[surfAddr[0]] = PueoTURFIO((dev, surfAddr[0]), 'TURFGTP')
        print(f'TURFIO#{surfAddr[0]} : {tio[surfAddr[0]]}')
        masks[surfAddr[0]] = 0
    masks[surfAddr[0]] |= 1<<(surfAddr[1])

for m in masks:
    print(f'autotrain {m} is {hex(masks[m])}')

# enable autotrain for the enabled SURFs
# and the COUT offset at the TURFIOs and the corresponding CIN offset
# at TURF. We can do this regardless of whether we're training
# the COUT path or not.
for n in tio:
    print(f'Setting TURFIO#{n} autotrain to {hex(masks[n])}')
    tio[n].surfturf.autotrain = masks[n]
    # magic number
    print(f'Setting TURFIO#{n} COUT offset to 3')
    tio[n].surfturf.cout_offset = 3
    print(f'Setting TURF CIN[{n}] offset to 0')
    # magic number 2
    dev.ctl.tio[n].cin_offset = 0

# enable RXCLK for the TURFIOs containing the SURFs
for t in tio.values():
    print(f'Enabling RXCLK on {t}')
    t.enable_rxclk(True)

surfActiveList = []
for surfAddr in surfList:
    tn = surfAddr[0]
    sn = surfAddr[1]
    # wait for train out rdy on each
    print(f'Waiting for train out rdy on SURF#{sn} on TURFIO#{tn}')
    loopno = 0
    while not(tio[tn].surfturf.train_out_rdy & (1<<sn)) and loopno < 20:
        time.sleep(0.1)
    if loopno == 20:
        print(f'SURF#{sn} on TURFIO#{tn} did not become ready??')
    else:
        print(f'SURF#{sn} on TURFIO#{tn} is ready for out training')
        tio[tn].dalign[sn].train_enable = 0
        surfActiveList.append(surfAddr)

# dumbass hackery, since sync_offset should be constant
for surfAddr in surfActiveList:
    tn = surfAddr[0]
    sn = surfAddr[1]
    t = tio[tn]
    print(f'Applying sync offset to SURF#{sn} on TURFIO#{tn}')
    s = PueoSURF((t, sn), 'TURFIO')
    s.sync_offset = 7
    
print("Issuing SYNC")
dev.trig.runcmd(dev.trig.RUNCMD_SYNC)

# We should be able to COMPLETELY align the entire
# payload the same, because the only variation should come
# from slot in crate....
# this might be wrong because of left/right issues

# we need a blank starting point
surfEyes = []
surfCoutEyes = []
for i in range(4):
    stio = []
    scouttio = []
    for j in range(7):
        stio.append(None)
        scouttio.append(None)
    surfEyes.append(stio)
    surfCoutEyes.append(scouttio)

tioCompleteMask = [ 0, 0, 0, 0 ]
    
# Find ALL the eyes
for surfAddr in surfActiveList:
    tn = surfAddr[0]
    sn = surfAddr[1]
    t = tio[tn]    
    print(f'Finding DOUT alignment on SURF#{sn} on TURFIO#{tn}:')
    try:
        eyes = t.dalign[sn].find_alignment(do_reset=True)
    except IOError:
        print(f'DOUT alignment failed on SURF#{sn} on TURFIO#{tn}, skipping')
        continue
    print(f'DOUT alignment found eyes: {eyes}')
    if args.cout:
        try:
            coutEyes = t.calign[sn].find_alignment(do_reset=True)
        except IOError:
            print(f'COUT alignment failed on SURF#{sn} on TURFIO#{tn}, skipping')
            continue
        print(f'COUT alignment found eyes: {coutEyes}')
        surfCoutEyes[tn][sn] = coutEyes
    surfEyes[tn][sn] = eyes
    tioCompleteMask[tn] |= (1<<sn)

print('Eyes found, processing to find a common one.')
commonEye = None
for d in list(chain(*surfEyes)):
    if d is not None:
        commonEye = d.keys() if commonEye is None else commonEye & d.keys()
print(f'Common eye[s]: {commonEye}')

usingEye = None
if len(commonEye) > 1:
    print(f'Multiple common eyes found, choosing the one with smallest delay')
    test_surf = None
    for i in range(4):
        for j in range(7):
            if surfEyes[i][j] is not None:
                test_surf = surfEyes[i][j]
    min = None
    minEye = None
    for eye in commonEye:
        if minEye is None:
            min = test_surf[eye]
            minEye = eye
            print(f'First eye {minEye} has tap {min}')
        else:
            if test_surf[eye] < min:
                min = test_surf[eye]
                minEye = eye
                print(f'New eye {minEye} has smaller tap {min}, using it')
    usingEye = minEye
elif len(commonEye):
    usingEye = list(commonEye)[0]

if args.cout:
    commonCoutEye = None
    for d in list(chain(*surfCoutEyes)):
        if d is not None:
            commonCoutEye = d.keys() if commonCoutEye is None else commonCoutEye & d.keys()            
    print(f'Common COUT eye[s]: {commonCoutEye}')
    usingCoutEye = None
    if len(commonCoutEye)>1:
        print(f'Multiple common COUT eyes found, choosing the one with the smallest delay')
        test_surf = None
        for i in range(4):
            for j in range(7):
                if surfEyes[i][j] is not None:
                    test_surf = surfCoutEyes[i][j]
        min = None
        minEye = None
        for eye in commonCoutEye:
            if minEye is None:
                min = test_surf[eye]
                minEye = eye
                print(f'First eye {minEye} has tap {min}')
            else:
                if test_surf[eye] < min:
                    min = test_surf[eye]
                    minEye = eye
                    print(f'New eye {minEye} has smaller tap {min}, using it')
            usingCoutEye = minEye
    elif len(commonCoutEye):
        usingCoutEye = list(commonCoutEye)[0]

print(f'DOUT eye: {usingEye}')
if args.cout:
    print(f'COUT eye: {usingCoutEye}')

trainedSurfs = []

for i in range(4):
    for j in range(7):
        if surfEyes[i][j] is not None:
            eye = (surfEyes[i][j][usingEye], usingEye)
            tio[i].dalign[j].apply_alignment(eye)
            if args.cout:
                eye = (surfCoutEyes[i][j][usingCoutEye], usingCoutEye)
                tio[i].calign[j].apply_alignment(eye)
            trainedSurfs.append( (i, j) )
    if args.cout:
        print("Now aligning trigger inputs (CIN) at TURF:")
        for j in range(7):
            # if we got an eye we can train it at the TURF
            if surfCoutEyes[i][j] is not None:
                eye = dev.ctl.tio[i].bit[j].locate_eyecenter()
                print(f'TURFIO{i} SURF{j} : {eye[0]} ps {eye[1]} offset')
                dev.ctl.tio[i].bit[j].apply_eye(eye)
                        
# Enabling is a bit tricky, because we CANNOT
# enable the data path UNTIL the SURF exits
# training.
# The SURF live detector does this for us.
if args.enable:
    for i in range(4):
        if tioCompleteMask[i] != 0:
            print(f'Setting TURFIO#{i} complete to {hex(tioCompleteMask[i])}')
            tio[i].surfturf.train_complete = tioCompleteMask[i]
            
    print("Issuing NOOP_LIVE")
    dev.trig.runcmd(dev.trig.RUNCMD_NOOP_LIVE)

    # now wait...
    for i in range(4):
        if tioCompleteMask[i] != 0:
            nloops = 20
            while tio[i].surfturf.surf_live & tioCompleteMask[i] != tioCompleteMask[i] and nloops:
                time.sleep(0.1)
                nloops = nloops - 1
            if nloops == 0:
                print("An expected SURF did not become live:")
                print(f'Expected {hex(tioCompleteMask[i])}')
                print(f'Got : {hex(tio[i].surfturf.surf_live & tioCompleteMask[i])}')
                sys.exit(1)
            if tio[i].surfturf.surf_misaligned & tioCompleteMask[i]:
                print('A trained SURF is misaligned: {hex(tio[i].surfturf.surf_misaligned & tioCompleteMask[i])}')
                sys.exit(1)
            
    for surfAddr in trainedSurfs:
        tn = surfAddr[0]
        sn = surfAddr[1]
        t = tio[tn]
        print(f'Unmasking data from SURF#{sn} on TURFIO#{tn}')
        t.dalign[sn].enable = 1
        
