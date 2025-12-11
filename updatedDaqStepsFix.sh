taylor/ppython checkIfReady.py --tio 3 --slots $slots3
taylor/ppython checkIfReady.py --tio 2 --slots $slots2
taylor/ppython checkIfReady.py --tio 1 --slots $slots1
taylor/ppython checkIfReady.py --tio 0 --slots $slots0
taylor/ppython taylor/pingPongReq.py --tio 3 --slots $slots3
taylor/ppython taylor/pingPongReq.py --tio 2 --slots $slots2
taylor/ppython taylor/pingPongReq.py --tio 1 --slots $slots1
taylor/ppython taylor/pingPongReq.py --tio 0 --slots $slots0
taylor/ppython taylor/fwNext_All.py --tio 3 --fwslot $fwFlag --slots $slots3
taylor/ppython taylor/fwNext_All.py --tio 2 --fwslot $fwFlag --slots $slots2
taylor/ppython taylor/fwNext_All.py --tio 1 --fwslot $fwFlag --slots $slots1
taylor/ppython taylor/fwNext_All.py --tio 0 --fwslot $fwFlag --slots $slots0
taylor/ppython startup/turfManualStartup.py
taylor/ppython startup/surfStartup.py --tio 3 --slots $slots3 --enable
taylor/ppython startup/surfStartup.py --tio 2 --slots $slots2 --enable
taylor/ppython startup/surfStartup.py --tio 1 --slots $slots1 --enable
taylor/ppython startup/surfStartup.py --tio 0 --slots $slots0 --enable
taylor/ppython taylor/mtsAdvance.py --tio 3 --slots $slots3
taylor/ppython taylor/mtsAdvance.py --tio 2 --slots $slots2
taylor/ppython taylor/mtsAdvance.py --tio 1 --slots $slots1
taylor/ppython taylor/mtsAdvance.py --tio 0 --slots $slots0
taylor/ppython calfreeze/calfreeze.py 1 --tio 0 --slot 6 --paramfile taylor/rfdc_gen3.pkl  
taylor/ppython calfreeze/calfreeze.py 1 --tio 1 --slot 6 --paramfile taylor/rfdc_gen3.pkl  
taylor/ppython taylor/rfStartAll.py --tio 3 --slots $rfTrigSlots3
taylor/ppython taylor/rfStartAll.py --tio 2 --slots $rfTrigSlots2
taylor/ppython taylor/rfStartAll.py --tio 1 --slots $rfTrigSlots1
taylor/ppython taylor/rfStartAll.py --tio 0 --slots $rfTrigSlots0
taylor/ppython taylor/thresholdRFAll.py --threshold 7000 --subthreshold 5000 --tio 3 --slots $rfTrigSlots3 --unmask --nbeams 48
taylor/ppython taylor/thresholdRFAll.py --threshold 7000 --subthreshold 5000 --tio 2 --slots $rfTrigSlots2 --unmask --nbeams 48
taylor/ppython taylor/thresholdRFAll.py --threshold 7000 --subthreshold 5000 --tio 1 --slots $rfTrigSlots1 --unmask --nbeams 48
taylor/ppython taylor/thresholdRFAll.py --threshold 7000 --subthreshold 5000 --tio 0 --slots $rfTrigSlots0 --unmask --nbeams 48
taylor/ppython taylor/processorsOff_All.py --tio 3 --slots $slots3 --procOff $procOff
taylor/ppython taylor/processorsOff_All.py --tio 2 --slots $slots2 --procOff $procOff
taylor/ppython taylor/processorsOff_All.py --tio 1 --slots $slots1 --procOff $procOff
taylor/ppython taylor/processorsOff_All.py --tio 0 --slots $slots0 --procOff $procOff
taylor/ppython checkIfReady.py --tio 3 --slots $slots3
taylor/ppython checkIfReady.py --tio 2 --slots $slots2
taylor/ppython checkIfReady.py --tio 1 --slots $slots1
taylor/ppython checkIfReady.py --tio 0 --slots $slots0
