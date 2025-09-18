#!/bin/bash
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
taylor/ppython taylor/rfStartAll.py --tio 3 --slots 0,1,2,3,4,5 
taylor/ppython taylor/rfStartAll.py --tio 2 --slots 0,1,2,3,4,5 
taylor/ppython taylor/rfStartAll.py --tio 1 --slots 0,1,2,3,4,5,6 
taylor/ppython taylor/rfStartAll.py --tio 0 --slots 0,1,2,3,4,5,6 
taylor/ppython taylor/thresholdRFAll.py --threshold 13000 --subthreshold 11000 --tio 3 --slots 0,1,2,3,4,5 --unmask --nbeams 48
taylor/ppython taylor/thresholdRFAll.py --threshold 13000 --subthreshold 11000 --tio 2 --slots 0,1,2,3,4,5 --unmask --nbeams 48
taylor/ppython taylor/thresholdRFAll.py --threshold 13000 --subthreshold 11000 --tio 1 --slots 0,1,2,3,4,5,6 --unmask --nbeams 48
taylor/ppython taylor/thresholdRFAll.py --threshold 13000 --subthreshold 11000 --tio 0 --slots 0,1,2,3,4,5,6 --unmask --nbeams 48
