#!/bin/bash
while IFS= read -r line || [[ -n "$line" ]]; do
    echo -e "\n\033[1;34mNext command:\033[0m $line"
    
    read -p "Execute this line? [y/N/q to quit] " confirm < /dev/tty
   
    case "$confirm" in
        [Yy])
            echo -e "\033[1;32m--- End Output ---\033[0m"
            output=$(eval "$line" 2>&1)
            status=$?
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
            else
                echo -e "\033[1;31m Error: Command failed with exit code $status\033[0m"
            fi
            echo -e "\033[1;32m--- End Output ---\033[0m"

            if [ $errorCode -ne 0 ]; then
                python3 fixError.py $errorCode
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
