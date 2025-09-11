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
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/pueo/pyrfdc/libunivrfdc/
export PYTHONSTARTUP=$MYSTARTUP
export PYTHONPATH=$MYBASE/pyrfdc:$MYBASE/pueo-python:$MYBASE/pueo-utils/HskSerial:$MYBASE/pueo-utils/EventTester:$PYTHONPATH

# create a file to hold the status of where you left off 
progress_file=".progress"

# Info on start number/line number you are on
start_line=0
line_num=0

# Start a timer 
elapsed_time=0

# how many retries do you want to allow for
retry=3

# Start a counter for any and all errors 
errorCount=0

# Restart flag because the progress file holds info 
# This actually might be a little silly to do to be honest
if [[ " $@ " =~ " --restart " ]]; then
    echo "Fresh start!"
    rm -f "$progress_file"
fi

# Reboot the TURF because I'm annoyed I keep having to go back and forth with it
if [[ " $@ " =~ "--reboot" ]]; then
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

            # set starting variables per loop
            retrycount=0
            turfretry=0
            success=false
            errorCode=0
            pmbustry=0
            
            

            # while retries not exhausted
            while [ $retrycount -le $retry ]; do
                output=$(eval "$line" 2>&1)
                status=$?
                
                if [[ " $@ " =~ " --verbose " ]]; then
                    echo "$output"
                fi
        
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

                elif echo "$output" | grep -zq "SURF slot#[0-9]\+ on TURFIO port#[0-9]\+ is not accessible!"; then
                    echo -e "\033[1;31m SURF not booted properly. Attempting power cycle \033[0m"
                    sn=$(echo "$output" | grep -oP 'slot#\K\d+' | tail -n 1)
                    tn=$(echo "$output" | grep -oP 'port#\K\d+' | tail -n 1)
                    if [ "$pmbustry" -eq 0 ]; then; then
                        errorCode=50
                        pmbustry=1
                    else
                        errorCode=51
                    fi

                elif echo "$output" | grep -zq "SURF#[0-9]\+ on TURFIO#[0-9]\+ did not become ready!"; then
                    # THIS ONE IS RESTART!!!!!!
                    echo -e "\033[1;31m SURF not requesting training properly \033[0m"
                    
                    sn=$(echo "$output" | grep -oP 'SURF#\K\d+' | tail -n 1)
                    tn=$(echo "$output" | grep -oP 'TURFIO#\K\d+' | tail -n 1)
                    echo -e "$sn"
                    echo -e "$tn"

                    errorCode=51 
                elif echo "$output" | grep -zq "SURF slot#[0-9]\+ on TURFIO port#[0-9]\+ never requested in training!"; then 
                # SURF slot#1 on TURFIO port#3 is not accessible!
                    echo -e "\033[1;31m SURF never requested in training c.\033[0m"
                    sn=$(echo "$output" | grep -oP 'slot#\K\d+' | tail -n 1)
                    tn=$(echo "$output" | grep -oP 'port#\K\d+' | tail -n 1)

                    echo -e "$sn"
                    echo -e "$tn"
                    errorCode=51
                elif echo "$output" | grep -zq "SURF slot#[0-9]\+ on TURFIO port#[0-9]\+ never requested out training!"; then 
                # SURF slot#1 on TURFIO port#3 is not accessible!
                    echo -e "\033[1;31m SURF never requested out training c.\033[0m"
                    sn=$(echo "$output" | grep -oP 'slot#\K\d+' | tail -n 1)
                    tn=$(echo "$output" | grep -oP 'port#\K\d+' | tail -n 1)

                    echo -e "$sn"
                    echo -e "$tn"
                    errorCode=51
                elif echo "$output" | grep -zq "SURF SLOT#[0-9]\+ on TURFIO PORT#[0-9]\+ failed to respond"; then 
                    echo -e "\033[1;31m SURF never booted \033[0m"
                    sn=$(echo "$output" | grep -oP 'slot#\K\d+' | tail -n 1)
                    tn=$(echo "$output" | grep -oP 'port#\K\d+' | tail -n 1)

                    echo -e "$sn"
                    echo -e "$tn"
                    errorCode=50
                elif echo "$output" | grep -zq "TURFIO sync complete"; then 
                    echo -e "\033[1;32m Success TURFIO \033[0m"
                    success=true
                    break
                elif echo "$output" | grep -zq "A SURF failed to MTS align"; then
                    echo -e "\033[1;31m SURF failed MTS alignment.\033[0m"
                    errorCode=100
                elif echo "$output" | grep -zq "All trained SURFs are now live"; then 
                    echo -e "\033[1;32m Success SURF \033[0m"
                    success=true
                    break
                elif echo "$output" | grep -zq "All SURFs booted and ready"; then
                    echo -e "\033[1;32m Booted SURFS \033[0m"
                    success=true
                    break
                elif echo "$output" | grep -zq "All SURFs aligned to 120"; then 
                    echo -e "\033[1;32m Success SURF MTS \033[0m"
                    success=true
                    break
                else
                    errorCode=100
                fi
    

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
                    # echo -e "$cmd"
                    eval "$cmd"
                    if [ $errorCode -eq 100 ]; then
                        # Reset progress file to 0
                        echo 0 > "$progress_file"

                        # Reset counters
                        retrycount=0
                        turfretry=0
                        line_num=0

                        # Restart the script
                        exec "$0"
                        
                     
                    else
                        echo -e "\033[1;33m Restarting script from line $line_num...\033[0m"
                        ((retrycount++))
                    fi
                    ((errorCount++))
                    
                fi
            done 
            if [ "$success" = true ]; then
                echo $line_num > "$progress_file"
            else
                python3 fixError.py 100
                # Reset progress file to 0
                echo 0 > "$progress_file"

                # Reset counters
                retrycount=0
                turfretry=0
                line_num=0

                # Restart the script
                # exec "$0"
                ((errorCount++))
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

done < updatedDAQstart.sh
# Calculate the elapsed time

rm -f "$progress_file"
elapsed_seconds=$((SECONDS - start_time))

elapsed_formatted=$(date -ud "@$elapsed_seconds" +'%M min %S sec')
echo "DAQ set-up completed with $errorCount errors"
echo "Elapsed time: $elapsed_formatted"s