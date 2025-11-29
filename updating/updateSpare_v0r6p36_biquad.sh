#!/bin/bash

# turn on development mode
development_mode on
# replace the old software and firmware
cat /home/root/x* > /home/root/pueo_surf6_v0r6p36_bq2_36beam.bit.xz

rm /mnt/bitstreams/1/*

mv /mnt/bitstreams/0/*.xz /mnt/bitstreams/1/
cp /home/root/*.xz /mnt/bitstreams/0/
# sync to make sure everything finishes
sync
# turn off development mode
development_mode off
