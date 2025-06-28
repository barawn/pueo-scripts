#! /bin/bash

if [ $# -eq 0 ]
    then 
        echo "Starting up all TURFIOs"
        /home/pueo/taylor/ppython /home/pueo/startup/turfManualStartup
fi

while test $# -gt 0; do
    case $1 in 
        -t|--tio)
            shift
            /home/pueo/taylor/ppython /home/pueo/startup/turfManualStartup --turfio $1
            shift;;
    esac
done
