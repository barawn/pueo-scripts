#! /bin/bash

if [ $# -eq 0 ]
    then 
        echo "Starting up all TURFIOs"
        /home/pueo/taylor/ppython /home/pueo/startup/turfManualStartup.py
        /home/puep/taylor/ppython /home/pueo/startup/surfStartup.py --enable --tio 0 --slots 0,1,2,3,4,5,6
        /home/puep/taylor/ppython /home/pueo/startup/surfStartup.py --enable --tio 1 --slots 0,1,2,3,4,5,6
        /home/puep/taylor/ppython /home/pueo/startup/surfStartup.py --enable --tio 2 --slots 0,1,2,3,4,5
        /home/puep/taylor/ppython /home/pueo/startup/surfStartup.py --enable --tio 3 --slots 0,1,2,3,4,5
        /home/puep/taylor/ppython /home/pueo/startup/mtsAdcance.py
fi

while test $# -gt 0; do
    case $1 in 
        -t|--tio)
            shift
            /home/pueo/taylor/ppython /home/pueo/startup/turfManualStartup.py --turfio $1
            if $1 -eq 0; then
                /home/puep/taylor/ppython /home/pueo/startup/surfStartup.py --enable --tio 0 --slots 0,1,2,3,4,5,6
                /home/puep/taylor/ppython /home/pueo/startup/mtsAdcance.py --tio 0
            else if $1 -eq 1; then
                /home/puep/taylor/ppython /home/pueo/startup/surfStartup.py --enable --tio 1 --slots 0,1,2,3,4,5,6
                /home/puep/taylor/ppython /home/pueo/startup/mtsAdcance.py --tio 1
            else if $1 -eq 2; then
                /home/puep/taylor/ppython /home/pueo/startup/surfStartup.py --enable --tio 2 --slots 0,1,2,3,4,5
                /home/puep/taylor/ppython /home/pueo/startup/mtsAdcance.py --tio 2
            else if $1 -eq 3; then
                /home/puep/taylor/ppython /home/pueo/startup/surfStartup.py --enable --tio 3 --slots 0,1,2,3,4,5
                /home/puep/taylor/ppython /home/pueo/startup/mtsAdcance.py --tio 3
            shift;;

    esac
done
