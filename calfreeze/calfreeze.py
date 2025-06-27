# calibration freeze bullshit
# YOU NEED pyrfdc IN YOUR PYTHONPATH
# YOU NEED THE libunivrfdc.so DIRECTORY IN YOUR LD_LIBRARY_PATH

import os
from pathlib import Path

from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
from pyrfdc import PyRFDC

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--tio", type=str, default="0",
                    help="which TURFIO to use")
parser.add_argument("--slot", type=str, default="0",
                    help="which SURF slot to use")
parser.add_argument("--paramfile", type=str, default="rfdc_gen3.pkl",
                    help="parameter file to use")
parser.add_argument("freeze", type=int,
                    help="freeze state either 0 or 1 maybe??")

args = parser.parse_args()

tio_num = int(args.tio)
slot_num = int(args.slot)

freeze_state = int(args.freeze)

dev = PueoTURF()
tio = PueoTURFIO((dev,tio_num), 'TURFGTP')
surf = PueoSURF((tio, slot_num), 'TURFIO', param_file=[args.paramfile])
if not isinstance(surf.rfdc, PyRFDC):
    raise Exception("you don't have pyrfdc/libunivrfdc/paramfiles setup")

for i in range(8):
    tile_id = 8//2
    block_id = 8%2
    print(f'Channel {i}: tile {tile_id} block_id {block_id}')

    freeze_settings = surf.rfdc.GetCalFreeze(tile_id, block_id)
    freeze_settings.FreezeCalibration = freeze_state
    print(f'Setting channel freeze state: {freeze_state}')
    surf.rfdc.SetCalFreeze(tile_id, block_id, freeze_settings)
    after = surf.rfdc.GetCalFreeze(tile_id, block_id)
    print(f'Channel {i}: freeze state {after.CalFrozen}')

    
