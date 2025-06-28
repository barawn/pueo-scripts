#! /bin/bash

while getopts "tio:"; do
    case $arg in 
        tio)
            /home/pueo/taylor/ppython /home/pueo/startup/turfManualStartup --tio $OPTARG;;
    esac
done
if [ $OPTIND -eq 1 ]
    then 
        echo "Starting up all TURFIOs"
        /home/pueo/taylor/ppython /home/pueo/startup/turfManualStartup
fi

##ppython ../startup/turfManualStartup 