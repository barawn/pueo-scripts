#!/bin/bash

# turn on development mode
development_mode on
# replace the old software and firmware
rm /mnt/bitstreams/1/*
cat /home/root/xa{a..b} > /home/root/pueo_surf6_v0r6p34_bq2.bit.xz
mv /home/root/pueo_surf6_v0r6p34_bq2.bit.xz /mnt/bitstreams/1/

# sync to make sure everything finishes
sync
# turn off development mode
development_mode off
