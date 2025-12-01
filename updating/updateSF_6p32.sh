#!/bin/bash

# turn on development mode
development_mode on
# replace the old software and firmware


# Move no-biquad version to /1/
rm /mnt/bitstreams/1/*.xz
mv /mnt/bitstreams/0/*.bit.xz /mnt/bitstreams/1/

# Move new biquad version to /0/
mv /home/root/pueo_surf6_v0r6p32.bit.xz /mnt/bitstreams/0/

# sync to make sure everything finishes
sync
# turn off development mode
development_mode off
