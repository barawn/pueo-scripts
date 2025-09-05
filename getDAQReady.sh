#!/bin/bash

# A lot of this is adapted from Jim's stepRunner.sh
# Also I do not understand bash very well so uh 
# internet (lets be honest copilot) was heavily used 
# I am not ashamed (yes i am)

# From Patrick's ppython 
MYBASE=/home/pueo
MYSTARTUP=/home/pueo/pueo-scripts/taylor/ppy_startup.py
export PYTHONSTARTUP=$MYSTARTUP
export PYTHONPATH=$MYBASE/pyrfdc:$MYBASE/pueo-python:$MYBASE/pueo-utils/HskSerial:$MYBASE/pueo-utils/EventTester:$PYTHONPATH

progress_file=".progress"
start_line=0

# Check for restart flag
if [[ "$1" == "--restart" ]]; then
    echo "Restarting from beginning..."
    rm -f "$progress_file"
fi

if [ -f "$progress_file" ]; then
    start_line=$(cat "$progress_file")
fi

line_num=0
retry=3

while IFS= read -r line || [[ -n "$line" ]]; do
    echo -e "\n\033[1;34mNext command:\033[0m $line"

    ((line_num++))

    # Skip lines already processed
    # lets see if that actually works?
    if [ $line_num -le $start_line ]; then
        continue
    fi

    read -p "Execute this line? [y/N/q to quit] " confirm < /dev/tty

    case "$confirm" in
        [Yy])
            echo -e "\033[1;32m--- Output ---\033[0m"
            retrycount=0
            success=false
            errorCode=0
            while [ $retrycount -le $retry ]; do
                output=$(eval "$line" 2>&1)
                status=$?
                
                
                echo "$output"
                if echo "$output" | grep -q "TURFIO bridge error"; then
                    echo -e "\033[1;31 Detected TURFIO bridge error. Consider rebooting the TURF.\033[0m"
                elif echo "$output" | grep -q "GTP link 0"; then
                    echo -e "\033[1;31m Detected GTP link 0 error. Attempting error handling now!.\033[0m"
                    errorCode=1
                elif echo "$output" | grep -q "GTP link 1"; then
                    echo -e "\033[1;31m Detected GTP link 1 error. Attempting error handling now!.\033[0m"
                    errorCode=2
                elif echo "$output" | grep -q "GTP link 2"; then
                    echo -e "\033[1;31m Detected GTP link 2 error. Attempting error handling now!.\033[0m"
                    errorCode=3
                elif echo "$output" | grep -q "GTP link 3"; then
                    echo -e "\033[1;31m Detected GTP link 3 error. Attempting error handling now!.\033[0m"
                    errorCode=4
                elif [ $status -eq 0 ]; then
                    echo -e "\033[1;32m Success\033[0m"
                    success=true
                    break
                else
                    errorCode=100
                fi
                echo -e "\033[1;32m--- End Output ---\033[0m"

                if [ $errorCode -ne 0 ]; then
                    python3 fixError.py $errorCode
                    echo -e "\033[1;33m Restarting script from line $line_num...\033[0m"
                    ((retry_count++))
                    
                fi
            done 
            if [ "$success" = true ]; then
                echo $line_num > "$progress_file"
            else
                echo -e "\033[1;32m Success\033[0m"
                python3 fixError.py 100
                echo $line_num > "$progress_file"
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
