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


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("--turfio", type=str, default="0,1,2,3",
                    help="comma-separated list of TURFIOs to initialize")
parser.add_argument("--boring",
                    action='store_true',
                    help='make the output boring')

args = parser.parse_args()
color = exciting if not args.boring else boring

validTios = [0,1,2,3]
tioList = list(map(int,args.turfio.split(',')))
for tio in tioList:
    if tio not in validTios:
        print(color.BOLD + color.RED +
              f'TURFIOs can only be one of {validTios}' +
              color.END)
        sys.exit(1)

# get all the objects
dev = PueoTURF(None, 'Ethernet')
tios = [ None, None, None, None ]

for tionum in tioList:
    print(f'Getting TURFIO#{tionum}')
    try:
        tio = PueoTURFIO((dev, tionum), 'TURFGTP')
        tios[tionum] = tio
    except Exception as e:
        print(color.RED + color.BOLD +
              f'Getting TURFIO#{tionum} failed: {repr(e)}' +
              color.END)
        print(f'Exiting for debugging/fix.')
        exit(1)

for i in range(4):
    if tios[i]:
        tio = tios[i]
        tio.watchdog_disable = 1
        with tio.genspi as spi: 
            spi.program_mcs(args.filename) 
        tio.watchdog_disable = 0
        print(f'TURFIO#{i} has been successfully updated! Watchdog enabled.')
    else:
        print(f'Skipping TURFIO#{i} as it was not requested.')
