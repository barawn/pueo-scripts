#!/bin/bash
echo "Have you rebooted the TURF? If not exit and run minicom."
taylor/ppython startup/turfManualStartup.py 
taylor/ppython taylor/pingPongReq.py
taylor/ppython startup/surfStartup.py --tio 3 --slots 0,1,2,3,4,5 --enable
taylor/ppython startup/surfStartup.py --tio 2 --slots 0,1,2,3,4,5 --enable
taylor/ppython startup/surfStartup.py --tio 1 --slots 0,1,2,3,4,5,6 --enable
taylor/ppython startup/surfStartup.py --tio 0 --slots 0,1,2,3,4,5,6 --enable
taylor/ppython taylor/mtsAdvance.py --tio 3 
taylor/ppython taylor/mtsAdvance.py --tio 2
taylor/ppython taylor/mtsAdvance.py --tio 1
taylor/ppython taylor/mtsAdvance.py --tio 0
taylor/ppython calfreeze/calfreeze.py 1 --tio 0 --slot 6 --paramfile taylor/rfdc_gen3.pkl  
taylor/ppython calfreeze/calfreeze.py 1 --tio 1 --slot 6 --paramfile taylor/rfdc_gen3.pkl  

# taylor/ppython taylor/runEvent.py --stop 1 --filename softCheck
# taylor/ppython taylor/rfStartAll.py --tio 3 --slots 4,5
# taylor/ppython taylor/thresholdRFAll.py --threshold 19000 --tio 3 --slots 4,5 --freeze
# taylor/ppython taylor/beamLevelCheckAll.py --tio 3 --slots 4,5
# taylor/ppython taylor/rftrigger.py --stop 1 --filename rfCheck
