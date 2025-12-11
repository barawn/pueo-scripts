#!/bin/bash
development_mode on
cp /home/root/pueo_surf_v0r6p1.sqfs /mnt/pueo.sqfs
rm /tmp/pueo/next
ln -s /home/root/pueo_surf_v0r6p1.sqfs /tmp/pueo/next
sync
development_mode off
