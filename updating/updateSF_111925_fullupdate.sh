#!/bin/bash

# turn on development mode
development_mode on
# replace the old software and firmware
cp /home/root/pueo_surf_v0r7p4.sqfs /mnt/pueo.sqfs
rm /mnt/bitstreams/0/*
rm /mnt/bitstreams/1/*
xzcat /home/root/pueo_surf6_v0r6p30.bit.xz > /lib/firmware/pueo_surf6_v0r6p30.bit
mv /home/root/pueo_surf6_v0r6p30.bit.xz /mnt/bitstreams/0/
mv /home/root/pueo_surf6_v0r6p32.bit.xz /mnt/bitstreams/1/

# update the next pointers
rm /lib/firmware/next
ln -s /lib/firmware/pueo_surf6_v0r6p30.bit /lib/firmware/next
rm /tmp/pueo/next
ln -s /home/root/pueo_surf_v0r7p4.sqfs /tmp/pueo/next
# sync to make sure everything finishes
sync
# turn off development mode
development_mode off
