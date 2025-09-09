#!/bin/bash

# A lot of this is adapted from Jim's stepRunner.sh
# and uses DAQstart.sh to run the steps line by line
# 
# Also I do not understand bash very well so uh 
# internet (lets be honest copilot) was heavily used 
# I am not ashamed (...yes i am)
#                                      - Taylor 

# From Patrick's ppython 
# just sources all the scripts that we will need 
MYBASE=/home/pueo
MYSTARTUP=/home/pueo/pueo-scripts/taylor/ppy_startup.py
export PYTHONSTARTUP=$MYSTARTUP
export PYTHONPATH=$MYBASE/pyrfdc:$MYBASE/pueo-python:$MYBASE/pueo-utils/HskSerial:$MYBASE/pueo-utils/EventTester:$PYTHONPATH

# create a file to hold the status of where you left off 
progress_file=".progress"

# Info on start number/line number you are on
start_line=0
line_num=0

# how many retries do you want to allow for
retry=3

# Restart flag because the progress file holds info 
if [[ "$1" == "--restart" ]]; then
    echo "Fresh start!"
    rm -f "$progress_file"
fi

# Reboot the TURF 
if [[ "$2" == "--reboot" ]]; then
    echo "Rebooting TURF!" 
    errorCode=100
    python3 fixError.py $errorCode
fi

# Detect if there is a progress file
if [ -f "$progress_file" ]; then
    start_line=$(cat "$progress_file")
fi

# Begin the loop, yo! 
while IFS= read -r line || [[ -n "$line" ]]; do
    echo -e "\n\033[1;34mNext command:\033[0m $line"

    # hold what line number you are on every time you come back up here
    ((line_num++))

    if [ $line_num -le $start_line ]; then
        continue
    fi

    read -p "Execute this line? [y/N/q to quit] " confirm < /dev/tty

    case "$confirm" in
        [Yy])
            echo -e "\033[1;32m--- Output ---\033[0m"

            # set starting variables per loop
            retrycount=0
            turfretry=0
            success=false
            errorCode=0
            sn=0 
            tn=0

            # while retries not exhausted
            while [ $retrycount -le $retry ]; do
                output=$(eval "$line" 2>&1)
                status=$?
                
                
                # echo "$output"
                if echo "$output" | grep -q "GTP link 0"; then
                    echo -e "\033[1;31m Detected GTP link 0 error.\033[0m"
                    errorCode=1
                elif echo "$output" | grep -q "GTP link 1"; then
                    echo -e "\033[1;31m Detected GTP link 1 error.\033[0m"
                    errorCode=2
                elif echo "$output" | grep -q "GTP link 2"; then
                    echo -e "\033[1;31m Detected GTP link 2 error.\033[0m"
                    errorCode=3
                elif echo "$output" | grep -q "GTP link 3"; then
                    echo -e "\033[1;31m Detected GTP link 3 error.\033[0m"
                    errorCode=4
                elif echo "$output" | grep -q "TURFIO bridge error"; then
                    echo -e "\033[1;31 Detected TURFIO bridge error.\033[0m"
                    errorCode=100
                elif echo "$output" | grep -q "is not accessible!"; then

                    echo -e "\033[1;31m SURF not booted properly.\033[0m"

                    sn=$(echo "$output" | grep -oP 'slot#\K[0-9]+')
                    tn=$(echo "$output" | grep -oP 'port#\K[0-9]+')
                    errorCode = 50 
                elif echo "$output" | grep -q "did not become ready"; then

                    echo -e "\033[1;31m SURF not booted properly.\033[0m"
                    
                    sn=$(echo "$output" | grep -oP 'slot#\K[0-9]+')
                    tn=$(echo "$output" | grep -oP 'port#\K[0-9]+')
                    errorCode = 51 
                elif [ "$status" -eq 0 ]; then
                    echo "DEBUG: status=$status"
                    echo -e "\033[1;32m Success\033[0m"
                    success=true
                    break
                else
                    errorCode=99
                fi
                echo -e "\033[1;32m--- End Output ---\033[0m"

                if [ $errorCode -ne 0 ]; then
            
                    cmd="python3 -c 'from fixError import handle_error; handle_error($errorCode"

                    # Add tio if it's set
                    if [ -n "$tn" ]; then
                        cmd+=", tio=$tn"
                    fi

                    # Add slot if it's set
                    if [ -n "$sn" ]; then
                        cmd+=", slot=$sn"
                    fi
                    
                    cmd+=")'"

                    eval "$cmd"

                    echo -e "\033[1;33m Restarting script from line $line_num...\033[0m"
                    ((retrycount++))
                    
                fi
            done 
            if [ "$success" = true ]; then
                echo $line_num > "$progress_file"
            else
                echo -e "\033[1;32m Success\033[0m"
                python3 fixError.py 100
                echo $line_num > "$progress_file"
                retrycount=0
                ((turfretry++))
            fi
            ;;
    [Qq])
            echo -e "\033[1;31mQuitting...\033[0m"
            break
            ;;
        *)
            echo -e "\033[1;33mSkipped.\033[0m"
            ;;
    esac

done < DAQstart.sh
