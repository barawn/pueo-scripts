#!/bin/bash
while IFS= read -r line || [[ -n "$line" ]]; do
    echo -e "\n\033[1;34mNext command:\033[0m $line"
    
    read -p "Execute this line? [y/N/q to quit] " confirm < /dev/tty
    # if [[ "$confirm" =~ ^[Yy]$ ]]; then
    #     echo -e "\033[1;32m--- Output ---\033[0m"
    #     eval "$line"
    #     echo -e "\033[1;32m--- End Output ---\033[0m"
    # else
    #     echo -e "\033[1;33mSkipped.\033[0m"
    # fi
    case "$confirm" in
        [Yy])
            echo -e "\033[1;32m--- Output ---\033[0m"
            eval "$line"
            echo -e "\033[1;32m--- End Output ---\033[0m"
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
