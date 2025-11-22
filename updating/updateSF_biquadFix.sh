#!/bin/bash

# turn on development mode
development_mode on
# replace the old software and firmware
mv /mnt/bitstreams/0/pueo_surf6_v0r6p30.bit.xz /mnt/bitstreams/1/
mv /mnt/bitstreams/1/pueo_surf6_v0r6p32.bit.xz /mnt/bitstreams/0/
# sync to make sure everything finishes
sync
# turn off development mode
development_mode off
