#!/usr/bin/env python3

from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from pueo.common.term import Term

import time
import sys
import argparse
from itertools import chain

TRAIN_WAIT_LOOPS = 40
ALIGN_ATTEMPTS = 5

class exciting:
    PURPLE = Term.PURPLE
    CYAN = Term.CYAN
    DARKCYAN = Term.DARKCYAN
    BLUE = Term.BLUE
    GREEN = Term.GREEN
    YELLOW = Term.YELLOW
    RED = Term.RED
    BOLD = Term.BOLD
    UNDERLINE = Term.UNDERLINE
    END = Term.END

class boring:
    PURPLE = ''
    CYAN = ''
    DARKCYAN = ''
    BLUE = ''
    GREEN = ''
    YELLOW = ''
    RED = ''
    BOLD = ''
    UNDERLINE = ''
    END = ''

parser = argparse.ArgumentParser()
parser.add_argument("--enable",
                    action='store_true',
                    help='enable the datapath on SURFs at exit')
parser.add_argument('--auto',
                    action='store_true',
                    help='use autotrain instead of check for train in req')

parser.add_argument("--tio", type=int)
parser.add_argument("--slots", type=str, default="0,1,2,3,4,5,6")
parser.add_argument("--commandonly",
                    action='store_true',
                    help='only enable the commanding path')
parser.add_argument("--boring",
                    action='store_true',
                    help='make the output boring')
parser.add_argument("--noturf",
                    action='store_true',
                    help="don't train the TURF inputs, just TURFIO")
parser.add_argument("--manual")

args = parser.parse_args()
color = exciting if not args.boring else boring

slotList = list(map(int,args.slots.split(',')))

if args.tio:
    tio = args.tio
else:
    tio = 0

if args.manual: 
    print(color.BOLD + color.RED +'Manual arg is deprecated. Stop using it. >:(' +
              color.END)

surfList = []
for slot in slotList:
    surfList.append( (tio, slot) )

dev = PueoTURF(None, 'Ethernet')
tio = {}
masks = {}
for surfAddr in surfList:
    if surfAddr[0] not in tio:
        print(f'Building TURFIO port#{surfAddr[0]}')
        try:
            tio[surfAddr[0]] = PueoTURFIO((dev, surfAddr[0]), 'TURFGTP')
        except Exception as e:
            print(color.BOLD + color.RED +
                  f'Could not build TURFIO port#{surfAddr[0]} : {repr(e)}' +
                  color.END)
            exit(1)
        print(f'TURFIO port#{surfAddr[0]} : {tio[surfAddr[0]]}')
        masks[surfAddr[0]] = 0
    print(f'Pulling TURFIO port#{surfAddr[0]} slot {surfAddr[1]} ISERDES out of reset')
    tio[surfAddr[0]].dalign[surfAddr[1]].iserdes_reset = 0
    masks[surfAddr[0]] |= 1<<(surfAddr[1])
    

for m in masks:
    print(f'Bitmask of SURFs to startup in TURFIO port#{m} is {hex(masks[m])}')

for n in tio:
    if not args.auto:
        print(f'Clearing TURFIO port#{n} autotrain bits: {hex(masks[n])}')
        r = tio[n].surfturf.autotrain
        m = masks[n] ^ 0xFF
        r = r & m     
    else:
        print(f'Setting TURFIO port#{n} autotrain bits: {hex(masks[n])}')
        r = tio[n].surfturf.autotrain
        r |= masks[n]
           
    print(f'TURFIO port#{n} autotrain bits now: {hex(r)}')
    tio[n].surfturf.autotrain = r

# Reset the live detector
for n in tio:
    tio[n].surfturf.livedet_reset = 1
    tio[n].surfturf.livedet_reset = 0
        
# enable RXCLK for the TURFIOs containing the SURFs
for n in tio:
    r = tio[n].surfturf.rxclk_disable
    m = masks[n] ^ 0xFF
    r = r & m
    print(f'Setting rxclk disable to {hex(r)}')
    tio[n].surfturf.rxclk_disable = r

# SURF STATE:
# At this point they should advance from 1 (WAIT_CLOCK)
# through to 9 (WAIT_CIN_ACTIVE) all by themselves.
# It may take a second or two.

# So if you exit here, SURFs should be in 9 (WAIT_CIN_ACTIVE) after a
# brief delay.
    
# OK, so what we're going to do here is go through and look
# for the SURFs requesting in training. The SURFs do this
# after they have seen the clock, programmed their own, and
# are up and running.
#
# If not all the SURFs we *expect* are there, we can exit now.
# The clocks for the others are still on, but that's fine.
# Rerunning this script after fixing is fine.

# objects are cool: just store them.
# the train_enable/oserdes_reset in dalign/calign are common.
# so we just grab the daligns.
daligns = []
surfActiveList=[]
anyTrain=False
st = time.time()
if not args.auto:
    # wait for train in req on each
    for surfAddr in surfList:
        tn = surfAddr[0]
        sn = surfAddr[1]
        print(f'Waiting for train in req on SURF slot#{sn} on TURFIO port#{tn}')
        loopno = 0
        # it should take a few seconds because it needs to program its clocks
        while not(tio[tn].surfturf.train_in_req & (1<<sn)) and loopno < TRAIN_WAIT_LOOPS:
            time.sleep(0.1)
            loopno = loopno + 1
        if loopno == TRAIN_WAIT_LOOPS:
            print(color.BOLD + color.RED +
                  f'SURF slot#{sn} on TURFIO port#{tn} never requested in training!'+
                  color.END)
            print('Exiting to allow fixes/debugging.')
            exit(1)
        if not anyTrain:
            anyTrain = True
            sp = time.time()
            print(f'Waited {sp-st} for first SURF to request in training.')
        print(color.GREEN +
              f'SURF slot#{sn} on TURFIO port#{tn} is requesting in training' +
              color.END)
        print(f'SURF train out rdy: {hex(tio[tn].surfturf.train_out_rdy)}')
        daligns.append(tio[tn].dalign[sn])
        surfActiveList.append((tn,sn))

# SURFs are DEFINITELY in state 9 (WAIT_CIN_ACTIVE) now.
        
# In training also tells us that they've handled their clocks:
# so we can check that the SURFs exist here.
for surfAddr in surfActiveList:
    tn = surfAddr[0]
    sn = surfAddr[1]
    t = tio[tn]
    s = PueoSURF((t,sn), 'TURFIO')
    if s.read(0).to_bytes(4,'big') != b'SURF':
        print(color.BOLD + color.RED +
              f'SURF slot#{sn} on TURFIO port#{tn} is not accessible!' +
              color.END)
        print('Exiting to allow checks/fixes.')
        exit(1)
    print(f'Slot #{sn} is a SURF: applying sync offset')
    s.sync_offset = 7

# At this point the SURFs exist. Turn on the outputs
for align in daligns:
    align.train_enable = 1
    align.oserdes_reset = 0

# SURF STATE HERE:
# SURFs should advance from 9 to 14 all by themselves.

# Wait for out train request. 
surfActiveList = []
daligns = []
st = time.time()
anyTrain = False
for surfAddr in surfList:
    tn = surfAddr[0]
    sn = surfAddr[1]
    # wait for train out rdy on each
    print(f'Waiting for train out rdy on SURF#{sn} on TURFIO#{tn}')
    loopno = 0
    while not(tio[tn].surfturf.train_out_rdy & (1<<sn)) and loopno < TRAIN_WAIT_LOOPS:
        time.sleep(0.1)
        loopno = loopno + 1
    if loopno == TRAIN_WAIT_LOOPS:
        print(color.BOLD + color.RED +
              f'SURF#{sn} on TURFIO#{tn} did not become ready!' +
              color.END)
        print('Exiting to allow checks/fixes.')
        exit(1)
    else:
        if not anyTrain:
            sp = time.time()
            anyTrain = True
            print(f'Waited {sp-st} for first SURF to finish in training')
        print(color.GREEN +
              f'SURF#{sn} on TURFIO#{tn} is ready for out training' +
              color.END)
        daligns.append(tio[tn].dalign[sn])
        surfActiveList.append(surfAddr)

# At this point the SURFs are DEFINITELY in state 14.
        
# This is the point of no return - once we turn off train
# enable from a TURFIO, they're getting commanding from the TURFs
# so now we have to be a ton more careful if we repeat things.
for align in daligns:
    align.train_enable = 0
    
print("Issuing SYNC!")
dev.trig.runcmd(dev.trig.RUNCMD_SYNC)

# This is ALL THAT'S NEEDED for command-only.
if args.commandonly:
    print('Exiting because requested command-only startup.')
    print('These SURFs will not produce valid data or triggers!')
    exit(0)
    
print(f'Training the outbound (DOUT/COUT) paths from the SURFs.')
# we need a blank starting point
doutEyes = []
coutEyes = []
for i in range(4):
    dtio = []
    ctio = []
    for j in range(7):
        dtio.append(None)
        ctio.append(None)
    doutEyes.append(dtio)
    coutEyes.append(ctio)

tioCompleteMask = [ 0, 0, 0, 0 ]    
# Find ALL the eyes
eyesFound = False
for surfAddr in surfActiveList:
    tn = surfAddr[0]
    sn = surfAddr[1]
    t = tio[tn]
    print(f'Finding alignments on SURF#{sn} on TURFIO#{tn}:')
    dtries = 0
    while dtries < ALIGN_ATTEMPTS:
        try:
            deyes = t.dalign[sn].find_alignment(do_reset=True)
            break
        except IOError:
            print(f'Attempt {dtries+1} at aligning DOUT failed on SURF#{sn} TURFIO#{tn}')
            dtries = dtries + 1
    ctries = 0
    while ctries < ALIGN_ATTEMPTS:
        try:
            ceyes = t.calign[sn].find_alignment(do_reset=True)
            break
        except IOError:
            print(f'Attempt {ctries+1} at aligning COUT failed on SURF#{sn} TURFIO#{tn}')
            ctries = ctries + 1
    
    if dtries < ALIGN_ATTEMPTS and ctries < ALIGN_ATTEMPTS:
        print(color.GREEN +
              f'Alignments succeeded on SURF#{sn} TURFIO#{tn}' +
              color.END)
        print(f'DOUT alignment found eyes: {deyes}')
        print(f'COUT alignment found eyes: {ceyes}')
    
        doutEyes[tn][sn] = deyes
        coutEyes[tn][sn] = ceyes
        tioCompleteMask[tn] |= (1<<sn)
        eyesFound = True
    else:
        if dtries == ALIGN_ATTEMPTS:
            print(color.BOLD +
                  f'DOUT alignment failed on SURF#{sn} on TURFIO#{tn}!' +
                  color.END)
            print(color.BOLD + color.RED + 'Exiting!' + color.END) 
            sys.exit(1) 
        if ctries == ALIGN_ATTEMPTS:
            print(color.BOLD +
                  f'COUT alignment failed on SURF#{sn} on TURFIO#{tn}!' +
                  color.END)            
            print(color.BOLD + color.RED + 'Exiting!' + color.END) 
            sys.exit(1)
        print(f'Skipping SURF#{sn} on TURFIO#{tn} for remaining operations!')

if not eyesFound:
    print(color.BOLD + color.RED +
          f'No SURF eyes found! Exiting!' +
          color.END)
    exit(1)

print('Eyes found, processing to find a common one.')
commonDoutEye = None
commonCoutEye = None
for d in list(chain(*doutEyes)):
    if d is not None:
        commonDoutEye = d.keys() if commonDoutEye is None else commonDoutEye & d.keys()
for c in list(chain(*coutEyes)):
    if c is not None:
        commonCoutEye = c.keys() if commonCoutEye is None else commonCoutEye & c.keys()

print(f'Common DOUT eye[s]: {commonDoutEye}')
print(f'Common COUT eye[s]: {commonCoutEye}')

test_dout = None
test_cout = None
for i in range(4):
    for j in range(7):
        if doutEyes[i][j] is not None and coutEyes[i][j] is not None:
            test_dout = doutEyes[i][j]
            test_cout = coutEyes[i][j]

def find_eye(eyes, test, label):
    if len(eyes) > 1:
        print(f'Multiple {label} eyes found, choosing one with smallest delay')
        min = None
        minEye = None
        for eye in eyes:
            if minEye is None:
                min = test[eye]
                minEye = eye
                print(f'First {label} eye {minEye} has tap {min}')
            else:
                if test[eye] < min:
                    min = test[eye]
                    minEye = eye
                    print(f'New {label} eye {minEye} has smaller tap {min}, using it')
        return minEye
    elif len(eyes):
        return list(eyes)[0]

usingDoutEye = find_eye(commonDoutEye, test_dout, 'DOUT')
usingCoutEye = find_eye(commonCoutEye, test_cout, 'COUT')
    
trainedSurfs = []

for i in range(4):
    for j in range(7):
        if doutEyes[i][j] is not None and coutEyes[i][j] is not None:
            eye = (doutEyes[i][j][usingDoutEye], usingDoutEye)
            try:
                tio[i].dalign[j].apply_alignment(eye)
            except Exception as e:
                print(color.BOLD +
                      f'DOUT eye {eye} on SURF#{sn} on TURFIO#{tn}: {repr(e)}' +
                      color.END)
                continue
            eye = (coutEyes[i][j][usingCoutEye], usingCoutEye)
            try:
                tio[i].calign[j].apply_alignment(eye)
            except Exception as e:
                print(color.BOLD +
                      f'COUT eye {eye} on SURF#{sn} on TURFIO#{tn}: {repr(e)}' +
                      color.END)
                continue
            trainedSurfs.append( (i, j) )

if not args.noturf:
    for surf in trainedSurfs:
        tn = surf[0]
        sn = surf[1]
        print(f'Aligning SURF#{sn} on TURFIO#{tn} through to TURF')
        eye = dev.ctl.tio[tn].bit[sn].locate_eyecenter()
        print(f'At TURF: TURFIO{tn} SURF{sn} : {eye[0]} ps {eye[1]} offset')
        dev.ctl.tio[tn].bit[sn].apply_eye(eye)            
else:
    print('Skipping TURF input align due to user request!')

for i in range(4):
    if tioCompleteMask[i] != 0:
        print(f'Setting TURFIO#{i} complete to {hex(tioCompleteMask[i])}')
        r = tio[i].surfturf.train_complete
        r |= tioCompleteMask[i]
        tio[i].surfturf.train_complete = r
            
print("Issuing NOOP_LIVE")
dev.trig.runcmd(dev.trig.RUNCMD_NOOP_LIVE)

# The SURFs will NOW advance to state 15 (WAIT_SYNC).

# now wait...
for i in range(4):
    if tioCompleteMask[i] != 0:
        nloops = TRAIN_WAIT_LOOPS
        while ((tio[i].surfturf.surf_live & tioCompleteMask[i]) != tioCompleteMask[i]) and nloops:
            time.sleep(0.1)
            nloops = nloops - 1
        if nloops == 0:
            print(color.BOLD + color.RED +
                  "An expected SURF did not become live:" +
                  color.END)
            print(f'Expected {hex(tioCompleteMask[i])}')
            print(f'Got : {hex(tio[i].surfturf.surf_live & tioCompleteMask[i])}')
            sys.exit(1)
        if tio[i].surfturf.surf_misaligned & tioCompleteMask[i]:
            print(color.BOLD + color.RED +
                  'A trained SURF is misaligned: {hex(tio[i].surfturf.surf_misaligned & tioCompleteMask[i])}' +
                  color.END)
            sys.exit(1)

print(color.BOLD + color.GREEN +
      'All trained SURFs are now live.' + color.END)
            
if args.enable:                
    for surfAddr in trainedSurfs:
        tn = surfAddr[0]
        sn = surfAddr[1]
        t = tio[tn]
        print(f'Unmasking data from SURF#{sn} on TURFIO#{tn}')
        t.dalign[sn].enable = 1
        
