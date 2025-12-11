#!/bin/bash

# turn on development mode
development_mode on
# replace the old software and firmware
cp /home/root/pueo_surf_v0r7p3.sqfs /mnt/pueo.sqfs
rm /mnt/bitstreams/0/*.bit.xz
xzcat /home/root/pueo_surf6_v0r3p4.bit.xz > /lib/firmware/pueo_surf6_v0r3p4.bit
mv /home/root/pueo_surf6_v0r3p4.bit.xz /mnt/bitstreams/0/
# update the next pointers
rm /lib/firmware/next
ln -s /lib/firmware/pueo_surf6_v0r3p4.bit /lib/firmware/next
rm /tmp/pueo/next
ln -s /home/root/pueo_surf_v0r7p3.sqfs /tmp/pueo/next
# sync to make sure everything finishes
sync
# turn off development mode
development_mode off
