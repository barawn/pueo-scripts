
# Adapted from Taylor's currentVoltsTempTest script
from HskSerial import HskEthernet, HskPacket
import time
import os
import signal
import csv
import numpy as np
from datetime import datetime
import argparse

TIO_V = 12.0 # Nominal Voltage

def convert_turfio_current(raw):
    return ((raw * 105.84) / (2**12 * 0.125))

def convert_surf_current(raw):
    return ((raw - 2048) * 12.51 / 4.762)

def convert_turfio_temp(raw):
    return  (((raw * 503.975) / 2 ** 12) - 273.15)

def convert_surf_temp(raw):
    return ((raw * 10 - 31880) / 42)

def convert_turfio_voltage(raw):
    return (raw * 26.35 / 2 ** 12)

def convert_surf_voltage(raw):
    return (((raw + 0.5) * 5.104) / 1000)

parser = argparse.ArgumentParser()

parser.add_argument("--filename", type=str, default="hsk_data.csv")
parser.add_argument("--tioAddr", type=str, default="0x48")
parser.add_argument("--printOnly", action="store_true")
parser.add_argument("--printAll", action="store_true")
parser.add_argument("--mins", type=int, default=1)

args = parser.parse_args()

tio_addr = int(args.tioAddr,base=16)

hsk = HskEthernet()
hsk.send(HskPacket(tio_addr, 'eEnable', [0x40, 0x40]))
pkt = hsk.receive()
with open(args.filename, 'a', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # csv_writer.writerow(headers)
    for i in range(0,int((60/5)*args.mins)): 
       
        hsk.send(HskPacket(tio_addr, 'eVolts'))
        data_volts = hsk.receive().data

        hsk.send(HskPacket(tio_addr, 'eTemps'))
        data_temps = hsk.receive().data

        hsk.send(HskPacket(tio_addr, 'eCurrents'))
        data_currents = hsk.receive().data

        surfVolts = np.zeros(7)
        surfTemps = np.zeros(7)
        surfCurrents = np.zeros(7)
        surfWatts = np.zeros(7)
        for iter in range(0, 16, 2):
            volt_val = (int.from_bytes(data_volts[iter:iter+2], byteorder='big') )
            temp_val = (int.from_bytes(data_temps[iter:iter+2], byteorder='big') )
            current_val = (int.from_bytes(data_currents[iter:iter+2], byteorder='big') )

            if (iter==0):
                V = convert_turfio_voltage(volt_val)
                turfioVolt = V
                print('TURFIO:', round(V, 2), 'V')
            else:
                V = convert_surf_voltage(volt_val)
                surfVolts[int(iter/2)-1] = V
                if (V > 0 or args.printAll):
                    print('SURF slot ' + str(int(iter/2)-1) + ':', round(V, 2), 'V')

            if (iter==0):
                I = convert_turfio_current(current_val)
                W = TIO_V * (I/1000.0)
                turfioCurrent = I
                turfioWatt = W
                print('TURFIO:', round(I, 2), 'mA')
                print('TURFIO:', round(W, 2), 'W')
            else:
                I = convert_surf_current(current_val)
                W = TIO_V * (I/1000.0)
                surfCurrents[int(iter/2)-1] = I
                surfWatts[int(iter/2)-1] = W
                if (I > 0 or args.printAll):
                    print('SURF slot ' + str(int(iter/2)-1) + ':', round(I, 2), 'mA')
                    print('SURF slot ' + str(int(iter/2)-1) + ':', round(W, 2), 'W')

            if (iter==0):
                T = convert_turfio_temp(temp_val)
                turfioTemp = T
                print('TURFIO:', round(T, 2), 'C')
            else:
                T = convert_surf_temp(temp_val)
                surfTemps[int(iter/2)-1] = T
                if (T > 0 or args.printAll):
                    print('SURF slot ' + str(int(iter/2)-1) + ':', round(T, 2), 'C')

        print("**********************\n")
        
        ts = time.time()
        new_data = [datetime.fromtimestamp(ts).strftime('%H:%M:%S'), turfioVolt, surfVolts[4], surfVolts[5], turfioTemp, surfTemps[4], surfTemps[5], turfioCurrent, surfCurrents[4], surfCurrents[5], turfioWatt, surfWatts[4], surfWatts[5]]
        if(not args.printOnly):
            csv_writer.writerow(new_data)
        time.sleep(5)
