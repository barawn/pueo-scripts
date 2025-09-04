#!/bin/bash

# turn on development mode
development_mode on
# replace the old software and firmware
rm /mnt/bitstreams/1/*.bit.xz
mv /mnt/bitstreams/0/* /mnt/bitstreams/1/
xzcat /home/root/pueo_surf6_v0r4p22.bit.xz > /lib/firmware/pueo_surf6_v0r4p22.bit
mv /home/root/pueo_surf6_v0r4p22.bit.xz /mnt/bitstreams/0/
# update the next pointers
rm /lib/firmware/next
ln -s /lib/firmware/pueo_surf6_v0r4p22.bit /lib/firmware/next
# sync to make sure everything finishes
sync
# turn off development mode
development_mode off
