#!/bin/bash

# turn on development mode
development_mode on
# replace the old software and firmware
# rm /mnt/bitstreams/2/*
rm /mnt/bitstreams/1/*
rm /mnt/bitstreams/0/*
cat /home/root/x* > /home/root/pueo_surf6_v0r7p2.bit.xz
xzcat /home/root/pueo_surf6_v0r7p2.bit.xz > /lib/firmware/pueo_surf6_v0r7p2.bit
cp /home/root/pueo_surf6_v0r7p2.bit.xz /mnt/bitstreams/0/
# mv /mnt/bitstreams/0/* /mnt/bitstreams/1/
# update the next pointers
rm /lib/firmware/next
ln -s /lib/firmware/pueo_surf6_v0r7p2.bit /lib/firmware/next

# sync to make sure everything finishes
sync
# turn off development mode
development_mode off
