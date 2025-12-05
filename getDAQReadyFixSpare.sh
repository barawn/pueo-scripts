#!/bin/bash

# A lot of this is adapted from Jim's stepRunner.sh
# and uses DAQstart.sh to run the steps line by line
# 
# Also I do not understand bash very well so uh 
# internet (lets be honest copilot) was heavily used 
# I am not ashamed (...yes i am)
#                                      - Taylor 

# TO DO ON HERE: 
# []  Timeout --> maybe add a counter that maxes out after 5 minutes? 
# []  Restart Startup --> SURF Slot 5 is being real wonk. Let's fix that 
# [x] TURF someone stealing 

source configfile.conf

# switch to directory this is called from
cd "$(dirname "$0")"

# From Patrick's ppython 
# just sources all the scripts that we will need 
MYBASE=/home/pueo/surfcomm/
MYSTARTUP=/home/pueo/surfcomm/pueo-scripts/taylor/ppy_startup.py
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/pueo/surfcomm/pyrfdc/libunivrfdc/
export PYTHONSTARTUP=$MYSTARTUP
export PYTHONPATH=$MYBASE/pyrfdc:$MYBASE/pueo-python:$MYBASE/pueo-utils/HskSerial:$MYBASE/pueo-utils/EventTester:$PYTHONPATH

# create a file to hold the status of where you left off 
progress_file=".progress"

# Info on start number/line number you are on
start_line=0
line_num=0
keepError=0

# how many retries do you want to allow for
retry=2

# Start a counter for any and all errors 
if [ -f "keepError.txt" ]; then
    keepError=$(<keepError.txt)
fi


if [ -f "errorLog.txt" ]; then
    if [ $keepError -eq 0 ]; then
        rm -f "errorLog.txt"
    fi
fi 

if [ -f "errorCount.txt" ]; then
    errorCount=$(<errorCount.txt)
else
    errorCount=0
fi

if [ -f "startTime.txt" ]; then
    start_time=$(<startTime.txt)
else
    start_time=0
fi


# Restart flag because the progress file holds info
# This actually might be a little silly to do to be honest
if [ -f "$progress_file" ]; then
    rm -f "$progress_file"
fi

# Reboot the TURF because I'm annoyed I keep having to go back and forth with it
if [[ " $@ " =~ "--reboot" ]]; then
    errorCode=100
    python3 fixError.py $errorCode
fi

# if [[ " $@ " =~ " --fw0 " ]]; then
  #   fwFlag=0
#fi

#if [[ " $@ " =~ " --fw1 " ]]; then 
 #   fwFlag=1
#fi

#if [[ " $@ " =~ " --fw2 " ]]; then 
 #   fwFlag=2
#fi


# Detect if there is a progress file
if [ -f "$progress_file" ]; then
    start_line=$(cat "$progress_file")
fi

# Begin the loop, yo! 
while IFS= read -r line || [[ -n "$line" ]]; do
    
    # hold what line number you are on every time you come back up here
    ((line_num++))

    if [ $line_num -le $start_line ]; then
        continue
    fi

    # set starting variables per loop
    retrycount=0
    turfretry=0
    success=false
    errorCode=0
    pmbustry=0
    errorState=0

    # while retries not exhausted
    while [ $retrycount -le $retry ]; do
        output=$(eval "$line" 2>&1)
        status=$?
        # if [[ " $@ " =~ " --verbose " ]]; then
        echo "$output"
        # fi

        # TURF GTP Errors 
        if echo "$output" | grep -q "GTP link 0"; then
            echo -e "\033[1;31mDetected GTP link 0 error.\033[0m"
            errorCode=1
            errorState=1
            echo "$errorState" >> errorLog.txt
        elif echo "$output" | grep -q "GTP link 1"; then
            echo -e "\033[1;31mDetected GTP link 1 error.\033[0m"
            errorCode=2
            errorState=2 
            echo "$errorState" >> errrorLog.txt
        elif echo "$output" | grep -q "GTP link 2"; then
            echo -e "\033[1;31mDetected GTP link 2 error.\033[0m"
            errorCode=3
            errorState=3
            echo "$errorState" >> errorLog.txt
        elif echo "$output" | grep -q "GTP link 3"; then
            echo -e "\033[1;31mDetected GTP link 3 error.\033[0m"
            errorCode=4
            errorState=4
            echo "$errorState" >> errorLog.txt
        
        # TURFIO Bridge Errors
        elif echo "$output" | grep -q "TURFIO bridge error"; then
            echo -e "\033[1;31mDetected TURFIO bridge error.\033[0m"
            errorCode=99
            errorState=5 
            echo "$errorState" >> errorLog.txt

        # No clock align attempt
        elif echo "$output" | grep -q "RX clock off on all SURFs"; then
            echo -e "\033[1;31mNo clock alignment attempt detected.\033[0m"
            success=true
            break
        
        # Clock slip
        elif echo "$output" | grep -q "Clock not on correctly! Restart recommended"; then
            echo -e "\033[1;31mClock slip detected. TURF reboot required.\033[0m"
            errorCode=99
            errorState=6
            echo "$errorState" >> errorLog.txt
        
        # Only a partially finished clocking scheme
        elif echo "$output" | grep -q "RX clock off on only a few SURFs. Restart recommended!"; then
            echo -e "\033[1;31mOnly a few SURFs have Rx Clock enabled. TURF reboot required.\033[0m"
            errorCode=99
            errorState=7
            echo "$errorState" >> errorLog.txt
        
        # Clocking is done! 
        elif echo "$output" | grep -q "All trigger clocks are reporting on and no LOL"; then
            echo -e "\033[1;32mNo clock slips detected and system ready for RF data!\033[0m"
            success=true
            echo $line_num > "$progress_file"
            rm -f "$error_state"
            rm -f "$time_state"
            elapsed_seconds=$((SECONDS + startTime))
            elapsed_formatted=$(date -ud "@$elapsed_seconds" +'%M min %S sec')
            echo "DAQ set-up completed with $errorCount errors"
            echo "Elapsed time: $elapsed_formatted"s
            exit 0
        
        # Occasionally happens but tbh idk how to fix it
        elif echo "$output" | grep -zq "SURF slot#[0-9]\+ on TURFIO port#[0-9]\+ is not accessible!"; then
            echo -e "\033[1;31mSURF not booted.\033[0m"
            sn=$(echo "$output" | grep -oP 'slot#\K\d+' | tail -n 1)
            tn=$(echo "$output" | grep -oP 'port#\K\d+' | tail -n 1)
            if [ "$pmbustry" -eq 0 ]; then
                pmbustry=1
                if [ $fwFlag -eq 0 ]; then
                    errorCode=50
                elif [ $fwFlag -eq 1 ]; then
                    errorCode=51
                elif [ $fwFlag -eq 2 ]; then 
                    errorCode=52
                fi
                errorState=8
                errMessage="SURF $sn on TURFIO PORT#$tn: $errorState"
                echo "$errMessage" >> errorLog.txt
            else
                if [ $fwFlag -eq 0 ]; then
                    errorCode=60
                elif [ $fwFlag -eq 1 ]; then
                    errorCode=61
                elif [ $fwFlag -eq 2 ]; then 
                    errorCode=62
                fi
                errorState=9
                errMessage="SURF $sn on TURFIO PORT#$tn: $errorState"
                echo "$errMessage" >> errorLog.txt
            fi
        
        # Needs a restart
        elif echo "$output" | grep -zq "SURF#[0-9]\+ on TURFIO#[0-9]\+ did not become ready!"; then
            # eRestart
            echo -e "\033[1;31mSURF never requested in training\033[0m"
            sn=$(echo "$output" | grep -oP 'SURF#\K\d+' | tail -n 1)
            tn=$(echo "$output" | grep -oP 'TURFIO#\K\d+' | tail -n 1)
            if [ $fwFlag -eq 0 ]; then
              errorCode=60
            elif [ $fwFlag -eq 1 ]; then
              errorCode=61
            elif [ $fwFlag -eq 2 ]; then 
              errorCode=62
            fi
            errorState=9
            errMessage="SURF $sn on TURFIO PORT#$tn: $errorState"
            echo "$errMessage" >> errorLog.txt
        
        # Needs a restart but *different*
        elif echo "$output" | grep -zq "SURF slot#[0-9]\+ on TURFIO port#[0-9]\+ never requested in training!"; then 
            # eRestart
            echo -e "\033[1;31mSURF never requested in training c.\033[0m"
            sn=$(echo "$output" | grep -oP 'slot#\K\d+' | tail -n 1)
            tn=$(echo "$output" | grep -oP 'port#\K\d+' | tail -n 1)
            if [ $fwFlag -eq 0 ]; then
              errorCode=60
            elif [ $fwFlag -eq 1 ]; then
              errorCode=61
            elif [ $fwFlag -eq 2 ]; then 
              errorCode=62
            fi
            errorState=9
            errMessage="SURF $sn on TURFIO PORT#$tn: $errorState"
            echo "$errMessage" >> errorLog.txt
        
        # Third way a restart is needed 
        elif echo "$output" | grep -zq "SURF slot#[0-9]\+ on TURFIO port#[0-9]\+ never requested out training!"; then 
            # eRestart
            echo -e "\033[1;31m SURF never requested out training c.\033[0m"
            sn=$(echo "$output" | grep -oP 'slot#\K\d+' | tail -n 1)
            tn=$(echo "$output" | grep -oP 'port#\K\d+' | tail -n 1)
            if [ $fwFlag -eq 0 ]; then
              errorCode=60
            elif [ $fwFlag -eq 1 ]; then
              errorCode=61
            elif [ $fwFlag -eq 2 ]; then 
              errorCode=62
            fi
            errorState=9
            errMessage="SURF $sn on TURFIO PORT#$tn: $errorState"
            echo "$errMessage" >> errorLog.txt
        
        # Needs a power cycle
        elif echo "$output" | grep -zq "SURF SLOT#[0-9]\+ on TURFIO PORT#[0-9]\+ failed to respond"; then
            # ePMBus
            echo -e "\033[1;31mSURF did not boot properly \033[0m"
            sn=$(echo "$output" | grep -oP 'SLOT#\K\d+' | tail -n 1)
            tn=$(echo "$output" | grep -oP 'PORT#\K\d+' | tail -n 1)
            errorCode=49 #changed
            errorState=8
            errMessage="SURF $sn on TURFIO PORT#$tn: $errorState"
            echo "$errMessage" >> errorLog.txt
        
        # TURFIOs done! 
        elif echo "$output" | grep -zq "TURFIO sync complete"; then
            echo -e "\033[1;32mTURFIOs successfully clocking \033[0m"
            success=true
            break

        # MTS failed????
        elif echo "$output" | grep -zq "A SURF failed to MTS align"; then
            echo -e "\033[1;31mSURF failed MTS alignment\033[0m"
            errorCode=99
            errorState=10
            echo "$errState" >> errorLog.txt
        
        elif echo "$output" | grep -zq "Firmware loaded from /mnt/bitstreams/[0-9]\+"; then
            echo -e "\033[1;32mChanged the firmware \033[0m"
            success=true 
            break
        # SURFs done! 
        elif echo "$output" | grep -zq "All trained SURFs are now live"; then
            echo -e "\033[1;32mSURFs successfully clocking \033[0m"
            success=true
            break
        
        # SURFs powered on! 
        elif echo "$output" | grep -zq "All SURFs booted and ready"; then
            echo -e "\033[1;32mAll SURFs booted properly \033[0m"
            success=true
            break

        # MTS passed! 
        elif echo "$output" | grep -zq "All SURFs aligned to 120"; then
            echo -e "\033[1;32mMTS aligned to 120 \033[0m"
            success=true
            break
        
        # Cal path is done! 
        elif echo "$output" | grep -zq "Cal path frozen successfully"; then
            echo -e "\033[1;32mLF SURF cal path frozen \033[0m"
            success=true
            break

        # Enable trigger clocks
        elif echo "$output" | grep -zq "Okeedokee, clocks started, all beams unmasked!"; then
            echo -e "\033[1;32mRF Trigger clocks enabled \033[0m"
            success=true
            break
        
        # Set baseline thresholds, unmask beams
        elif echo "$output" | grep -zq "Yippee, threshold [0-9]\+ and subthreshold [0-9]\+"; then
            echo -e "\033[1;32mBaseline thresholds set and beams unmasked \033[0m"
            success=true
            break
        else
            errorCode=99
            exit 0 
        fi

        if [ $errorCode -ne 0 ]; then
            cmd="python3 -c 'from fixErrorFwSpare import handle_error; handle_error($errorCode"

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
            if [ $errorCode -eq 99 ]; then
                # Reset progress file to 0
                echo 0 > "$progress_file"
                exit 0
                # Reset counters
                retrycount=0
                turfretry=0
                line_num=0
                keepError=1
                echo "$keepError" > keepError.txt
                echo "$errorCount" > errorCount.txt
                echo "$startTime" > startTime.txt
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
        python3 fixErrorFwSpare.py 99
        # Reset progress file to 0
        echo 0 > "$progress_file"

        # Reset counters
        retrycount=0
        turfretry=0
        line_num=0

        # Restart the script
        ((errorCount++))
        echo "$errorCount" > errorCoutn.txt
        echo "$startTime" > startTime.txt
        exit 0
    fi
  

done < updatedDaqStepsFixSpare.sh
# Calculate the elapsed time

rm -f "$progress_file"
elapsed_seconds=$(( SECONDS + startTime ))

elapsed_formatted=$(date -ud "@$elapsed_seconds" +'%M min %S sec')
echo "DAQ set-up completed with $errorCount errors"
echo "Elapsed time: $elapsed_formatted"s

rm -f "$error_state"
rm -f "$time_state"
