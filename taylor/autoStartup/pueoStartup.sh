#! /bin/bash

STARTUP=/home/pueo/pueo-scripts/startup
TAYLOR=/home/pueo/pueo-scripts/taylor
PYTHON=$TAYLOR/ppython
if [ $# -eq 0 ]
    then

        echo "Restarting TURF"
        /home/pueo/pueo-scripts/ftdi-turf-restart.py --cpu || exit 1
        sleep 3

        until arping -I enp4s0f0 turf -c 1 ;
        do
          echo "Waiting for TURF..."
          sleep 5
        done
        echo "TURF up! Waiting another 20 seconds"
        sleep 30

        echo "Starting up all TURFIOs"
        $PYTHON $STARTUP/turfManualStartup.py || exit 1

        echo "Setting up HSK Bus"
        timeout -k 10 60 $PYTHON $TAYLOR/rUReadyKids.py || exit 1

        echo "Checking currents"
        $PYTHON $TAYLOR/getHSCurrents.py 0x40 || exit 1
        $PYTHON $TAYLOR/getHSCurrents.py 0x48 || exit 1
        $PYTHON $TAYLOR/getHSCurrents.py 0x50 || exit 1
        $PYTHON $TAYLOR/getHSCurrents.py 0x58 || exit 1

        echo "Aligning SURF clocks"
        $PYTHON $STARTUP/surfStartup.py --enable --tio 0 --slots 0,1,2,3,4,5,6 || exit 1
        $PYTHON $STARTUP/surfStartup.py --enable --tio 1 --slots 0,1,2,3,4,5,6 || exit 1
        $PYTHON $STARTUP/surfStartup.py --enable --tio 2 --slots 0,1,2,3,4,5 || exit 1
        $PYTHON $STARTUP/surfStartup.py --enable --tio 3 --slots 0,1,2,3,4,5 || exit 1


        $PYTHON $TAYLOR/mtsAdvance.py --tio 0 || exit 1
        $PYTHON $TAYLOR/mtsAdvance.py --tio 1 || exit 1
        $PYTHON $TAYLOR/mtsAdvance.py --tio 2 || exit 1
        $PYTHON $TAYLOR/mtsAdvance.py --tio 3 || exit 1

        exit
fi

while test $# -gt 0; do
    case $1 in 
        -t|--tio)
            shift
            /home/pueo/taylor/ppython /home/pueo/startup/turfManualStartup.py --turfio $1
            if [[ $1 -eq 0 ]]; then
                /home/pueo/taylor/ppython /home/pueo/startup/surfStartup.py --enable --tio 0 --slots 0,1,2,3,4,5,6 || exit 1
                /home/pueo/taylor/ppython /home/pueo/startup/mtsAdvance.py --tio 0 || exit 1
            else if [[ $1 -eq 1 ]]; then
                /home/pueo/taylor/ppython /home/pueo/startup/surfStartup.py --enable --tio 1 --slots 0,1,2,3,4,5,6 || exit 1
                /home/pueo/taylor/ppython /home/pueo/startup/mtsAdvance.py --tio 1 || exit 1
            else if [[ $1 -eq 2 ]]; then
                /home/pueo/taylor/ppython /home/pueo/startup/surfStartup.py --enable --tio 2 --slots 0,1,2,3,4,5 || exit 1
                /home/pueo/taylor/ppython /home/pueo/startup/mtsAdvance.py --tio 2 || exit 1
            else if [[ $1 -eq 3 ]]; then
                /home/pueo/taylor/ppython /home/pueo/startup/surfStartup.py --enable --tio 3 --slots 0,1,2,3,4,5 || exit 1
                /home/pueo/taylor/ppython /home/pueo/startup/mtsAdvance.py --tio 3 || exit 1
            fi
            shift;;
    esac
done
