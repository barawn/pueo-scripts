~/opython checkIfReady.py --tio 0 --slots $slots0
~/opython taylor/pingPongReq.py --tio $tio0 --slots 3,4
~/opython taylor/fwNext_All.py --tio $tio0 --slots 3,4 --fwslot $fwFlag
~/opython startup/turfManualStartup.py --turfio 0
~/opython startup/surfStartup.py --tio 0 --slots 3,4 --enable
~/opython taylor/mtsAdvance.py --tio $tio0 --slots $slots0
~/opython taylor/rfStartAll.py --tio 0 --slots $slots0
~/opython taylor/thresholdRFAll.py --threshold 7000 --subthreshold 5000 --tio 0 --slots $slots0 --unmask --nbeams 48
~/opython checkIfReady.py --tio 0 --slots $slots0
