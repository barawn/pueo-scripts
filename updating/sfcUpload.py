from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from HskSerial import HskEthernet, HskPacket

from hashlib import md5
import time

def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest() if ashexstr else hasher.digest()

def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)
            
def filemd5(fn):
    return hash_bytestr_iter(file_as_blockiter(open(fn, 'rb')),
                             md5(),
                             ashexstr=True)

# TURFIOs and SURFs MUST BE CONFIGURED
# AND ALIGNED. This uses the commanding path.
# No alignment = no commanding path!

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("--tio", type=str, default="0,1,2,3", 
        help="comma-separated list of TURFIOs to initialize")
parser.add_argument("--wait", type=int)
args = parser.parse_args()

print(f'Sending {args.filename} : MD5 {filemd5(args.filename)}')

# I SHOULD TAKE A JSON FILE TO CONFIGURE THIS
# I NEED:
# TURFIO SLOT #, HSK ADDRESS
# SURF SLOT #[s], HSK ADDRESS[es]
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
            (5, 0x85)] 
           # (6, 0x91)]
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
elif args.tio =='t':
    tios = (3, 0x48)
    surfs = [ (0, 0x93) ]
# get the housekeeping path
hsk = HskEthernet()
# make sure crate housekeeping is enabled
hsk.send(HskPacket(tios[1], 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()

# get the TURFIO
dev = PueoTURF(None, 'Ethernet')
tio = PueoTURFIO((dev, tios[0]), 'TURFGTP')
# get the SURFs and put in download mode.
# do this by taking it OUT of download mode first, then on.
surfList = []
surfAddrDict = {}
for s in surfs:
    surf = PueoSURF((tio, s[0]), 'TURFIO')
    # first turn off, just to be safe...
    hsk.send(HskPacket(s[1], 'eDownloadMode', data=[0]))
    pkt = hsk.receive()
    print("eDownloadMode off response:", pkt.pretty())
    surf.firmware_loading = 0
    # now turn on
    surf.firmware_loading = 1
    hsk.send(HskPacket(s[1], 'eDownloadMode', data=[1]))
    pkt = hsk.receive()
    print("eDownloadMode on response:", pkt.pretty())
    surfList.append(surf)
    surfAddrDict[surf] = s[1]

try:
    tio.surfturf.uploader.upload(surfList, args.filename)
except Exception as e:
    print("caught an exception during upload??")
    print(repr(e))
    
if args.wait:
    print(f'Waiting {args.wait} before getting journal')
    time.sleep(args.wait)
time.sleep(0.1)
for s in surfList:
    hsk.send(HskPacket(surfAddrDict[s], 'eJournal', data="-u pyfwupd -o cat -n 1"))
    pkt = hsk.receive()
    print("eJournal:", pkt.pretty(asString=True))
    
for s in surfList:
    hsk.send(HskPacket(surfAddrDict[s], 'eDownloadMode', data=[0]))
    pkt = hsk.receive()
    print("eDownloadMode response:", pkt.pretty())
    s.firmware_loading = 0

