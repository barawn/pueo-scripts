#! /usr/bin/env python3

import ftdi1
import argparse
import time
import sys

vid = 0x0403
pid = 0x6010
desc = 'Digilent Adept USB Device'
default_serial = '210203544604'

parser = argparse.ArgumentParser( prog = 'turf_reset.py',
                                  description = 'resets TURF via FT2322H' )

parser.add_argument('-s','--serial', default = default_serial)
parser.add_argument('-t','--cycletime', default = 0.1)
parser.add_argument('--cpu', action = 'store_true')
parser.add_argument('--power', action = 'store_true')

args = parser.parse_args()

reset_power = args.power
reset_cpu = args.cpu and not reset_power

if not reset_power and not reset_cpu:
    print("Nothing to do. Exiting.")
    sys.exit()

if reset_power:
    print("Resetting power")

if reset_cpu:
    print("Resetting CPU")

ser = args.serial
cycle_time = float(args.cycletime)

ctx = ftdi1.new()
if ctx is None:
    print ('Could not initialize FTDI Context')
    sys.exit(1)

ret = ftdi1.usb_open_desc(ctx, vid, pid, desc, ser);

if ret < 0:
    print ('Failed to open %x:%x desc=%s serial=%s' % (vid,pid,desc,ser))
    sys.exit(1)

ret = ftdi1.set_interface(ctx, ftdi1.INTERFACE_A)

if ret < 0:
    print ('Failed to select interface A')
    sys.exit(1)

ret = ftdi1.set_bitmode(ctx, 0, ftdi1.BITMODE_RESET)

if ret < 0:
    print('failed')
    sys.exit(1)

ret = ftdi1.set_bitmode(ctx, 0, ftdi1.BITMODE_MPSSE)

if ret < 0:
    print('failed')
    sys.exit(1)

if reset_cpu:
    # Pulling down either one of these pins resets the CPU
    # pull down ACBUS4 (pin 30)
    # cmd = [ftdi1.SET_BITS_HIGH, 0xef, 0x10]

    # pull down ACBUS5 (pin 32)
    cmd = [ftdi1.SET_BITS_HIGH, 0xdf, 0x20]
elif reset_power:
    # Pulling down either one of these pins shower power cycle
    # pull down ACBUS6 (pin 33)
    # cmd = [ftdi1.SET_BITS_HIGH, 0xbf, 0x40]

    # pull down ACBUS7 (pin 34)
    cmd = [ftdi1.SET_BITS_HIGH, 0x7f, 0x80]
else:
    cmd = []

written = ftdi1.write_data(ctx, bytes(cmd))

if written != len(cmd):
    print('Failed to write')
    sys.exit(1)

time.sleep(cycle_time)

# put all pins back to high-impedance
cmd = [ftdi1.SET_BITS_HIGH, 0x00, 0x00]
written = ftdi1.write_data(ctx, bytes(cmd))

if written != len(cmd):
    print('Failed to write')
    sys.exit(1)

ftdi1.usb_close(ctx)
ftdi1.free(ctx)

print("done")
