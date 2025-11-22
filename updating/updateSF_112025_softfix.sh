#!/bin/bash

# turn on development mode
development_mode on
# replace the old software and firmware
cp /home/root/pueo_surf_v0r7p8.sqfs /mnt/pueo.sqfs
# update the next pointers
rm /tmp/pueo/next
ln -s /home/root/pueo_surf_v0r7p8.sqfs /tmp/pueo/next
# sync to make sure everything finishes
sync
# turn off development mode
development_mode off
