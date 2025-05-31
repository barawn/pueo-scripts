#!/bin/bash
DIR=/mnt
development_mode on
for i in `find ${DIR}` ; do
    if [ -f $i ] ; then
	md5sum $i
    fi
done
development_mode off
