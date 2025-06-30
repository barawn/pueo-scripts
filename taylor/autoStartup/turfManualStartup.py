# this script assumes you're talking to the TURF via Ethernet
# ONLY DO THIS SCRIPT IF THE TURF STARTUP STATE MACHINE IS NOT DOING IT
#
# These commands CANNOT be repeated!! They're once-and-done!

from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.common.term import Term
import argparse
import sys

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

def turfManualStartup(tioList = [0, 1, 2, 3], termColor = True, verbose = False):
    color = exciting if termColor else boring

    validTios = [0,1,2,3]
    for tio in tioList:
        if tio not in validTios:
            print(color.BOLD + color.RED +
                f'TURFIOs can only be one of {validTios}' +
                color.END)
            return 1

    # get all the objects
    dev = PueoTURF(None, 'Ethernet')
    tios = [ None, None, None, None ]
    for tionum in tioList:
        if (verbose):
            print(f'Getting TURFIO#{tionum}')
        try:
            tio = PueoTURFIO((dev, tionum), 'TURFGTP')
            tios[tionum] = tio
        except Exception as e:
            print(color.RED + color.BOLD +
                f'Getting TURFIO#{tionum} failed: {repr(e)}' +
                color.END)
            print(f'Exiting for debugging/fix.')
            return 1

    # Start off by clean-resetting the TURF-y side stuff.
    dev.ctl.reset()

    for i in range(4):
        if tios[i]:
            tio = tios[i]
            if (verbose):
                print(f'Trying to initialize TURFIO#{i}')
            tio.program_sysclk(tio.ClockSource.TURF)
            while not ((tio.read(0xC) & 0x1)):
                if (verbose):
                    print(f'Waiting for clock on TURFIO#{i}...')
            if (verbose):
                print(f'Aligning RXCLK->SYSCLK transition on TURFIO#{i}...')
            tap = tio.cinalign.align_rxclk()
            if (verbose):
                print(f'TURFIO#{i} - tap is {tap}')
                print(f'Aligning CIN on TURFIO#{i}...')    
            dev.ctl.tio[i].train_enable(True)
        else:
            print(f'Skipping TURFIO#{i} as it was not requested.')

    tioEyes = [ None, None, None, None ]
    for i in range(4):
        if tios[i] is not None:
            try:
                eyes = tios[i].cinalign.find_alignment(do_reset=True)        
            except IOError:
                print(color.BOLD + color.RED +
                    f'Alignment failed on TURFIO#{i}, skipping' +
                    color.END)
                continue
            print(color.GREEN + f'CIN alignment found eyes: {eyes}' + color.END)
            tioEyes[i] = eyes

    if (verbose):
        print("Eyes found, processing to find a common one:")
    commonEye = None
    for d in tioEyes:
        if d is not None:
            commonEye = d.keys() if commonEye is None else commonEye & d.keys() 
    if (verbose):
        print(f'Common eye[s]: {commonEye}')
    usingEye = None
    if len(commonEye) > 1:
        if (verbose):
            print(f'Multiple common eyes found, choosing the one with smallest delay')
        test_turfio = None
        for i in range(4):
            if tioEyes[i] is not None:
                test_turfio = tioEyes[i]
                break
        min = None
        minEye = None
        for eye in commonEye:
            if minEye is None:
                min = test_turfio[eye]
                minEye = eye
                if (verbose):
                    print(f'First eye {minEye} has tap {min}')
            else:
                if test_turfio[eye] < min:
                    min = test_turfio[eye]
                    minEye = eye
                    if (verbose):
                        print(f'New eye {minEye} has smaller tap {min}, using it')
        usingEye = minEye
    elif len(commonEye):
        usingEye = list(commonEye)[0]

    if usingEye is None:
        print(color.BOLD + color.RED + "No common eye found???!?"
            + color.END)
        return 1

    if (verbose):
        print(f'Using eye: {usingEye}')

    aligned_turfios = []
    for i in range(4):
        if tioEyes[i] is not None:
            eye = (tioEyes[i][usingEye], usingEye)
            if (verbose):
                print(f'CIN alignment on TURFIO#{i}: tap {eye[0]} offset {eye[1]}')
            # I HATE YOU XILINX WHY DOESN'T THIS WORK CLEANLY
            trials = 0
            ok = False
            while not ok and trials < 1000:
                try:
                    tios[i].cinalign.apply_alignment(eye)
                    tios[i].cinalign.enable(True)
                    dev.ctl.tio[i].train_enable(False)
                    ok = True
                except Exception:
                    trials = trials + 1
            if trials == 1000:
                print(color.BOLD + color.RED +
                    f'CIN alignment on TURFIO#{i} failed?!?' +
                    color.END)
            else:
                print(color.GREEN +
                    f'CIN aligned and running on TURFIO#{i} after {trials} attempts' +
                    color.END)
                aligned_turfios.append(tios[i])
                

    for tio in aligned_turfios:    
        tio.syncdelay = 8        
        tio.extsync = True
        
    dev.trig.runcmd(dev.trig.RUNCMD_SYNC)
    for tio in aligned_turfios:
        tio.cinalign.oserdes_reset = 1
        tio.cinalign.oserdes_reset = 0
        tio.extsync = False
        
    print(color.BOLD + color.GREEN +
        f'TURFIO sync complete' +
        color.END)

    dev.dev.close()

    return 0

