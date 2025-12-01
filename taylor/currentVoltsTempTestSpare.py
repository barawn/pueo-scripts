from HskSerial import HskEthernet, HskPacket
import time
import csv
from datetime import datetime

filename = '/home/pueo/pueo-scripts/data/v0r6p34_unclocked_no_processors.csv'
stoptime = 600

processors_off=True

headers = [ 'tio','time', 'tfiov', 'sf0vin','sf0vout','sf1vin','sf1vout','sf2vin',
           'sf2vout','sf3vin','sf3vout','sf4vin','sf4vout','sf5vin','sf5vout',
           'sf6vin','sf6vout', 'tfiotemp', 'hs0temp','hs1temp','hs2temp', 'hs3temp',
           'hs4temp','hs5temp','hs6temp','apu0temp','apu1temp','apu2temp',
            'apu3temp','apu4temp','apu5temp','apu6temp', 'rpu0temp',
            'rpu1temp','rpu2temp','rpu3temp','rpu4temp','rpu5temp','rpu6temp',
            'tfiocurr', 'sf0curr','sf1curr','sf2curr','sf3curr','sf4curr',
            'sf5curr','sf6scurr' ]
hsk = HskEthernet()

tio0 = (0, 0x48)

surf3 = [(3, 0xa3),
         (4, 0xa4)]

tios = [tio0]
surfs = [surf3]


hsk.send(HskPacket(0x48, 'eEnable', data=[0x40, 0x40]))
pkt = hsk.receive()


def processorsOff(tio, surfs):
    for s in surfs:
        hsk.send(HskPacket(s[1], 'eSleep', data = [0x82]))
        pkt = hsk.receive()
        print(pkt.pretty())
    hsk.send(HskPacket(tio, 'eEnable', [0x40, 0x00])); pkt = hsk.receive()
    
    
def tfioVoltsEq(val): 
    return (val * 26.35 / 2 ** 12) 

def surfVoltsEq(val): 
    return (((val + 0.5) * 5.104) / 1000) 

def tfioTempEq(val): 
    return (((val * 503.975) / 2 ** 12) -273.15)

def hsTempEq(val): 
    return ((val * 10 - 31880) / 42)

def surfTempsEq(val):
    return ((val * 509.3140064) / 2 **16 - 280.23087870)

def tfioCurrentEq(val): 
    return ((val * 105.84) / (2**12 * 0.125))

def surfCurrentEq(val): 
    return ((val - 2048) * 12.51 / 4.762)

# start with processors off
for i in range(0,1): 
    tio = tios[i][1]
    surf = surfs[i]
    if processors_off:
        processorsOff(tio,surf)

with open(filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(headers)
    for times in range(0, stoptime):
        for i in [0]:#range(0,4): 
            tio = tios[i][1]
            surf = surfs[i]
            
            hsk.send(HskPacket(tio, 'eVolts'))
            data = hsk.receive().data
            # data = b'\x07:\x88 \x8b \x88\x80\x8b\x80\x88\x88\x8b\x88\x88"\x8b"\x88\x82\x8b\x82\x88\x8a\x8b\x8a\t\x1a\t\x18'
            
            turfioVolts = tfioVoltsEq(int.from_bytes(data[0:2],byteorder='big'))

            surfVolts = []
            for iter in range(2,30,2): 
                surfVolts.append(surfVoltsEq(int.from_bytes(data[iter:iter+2],byteorder='big')))

            hsk.send(HskPacket(tio, 'eTemps'))
            data = hsk.receive().data
            # data = b'\n\x8c\x8d \x8d\x80\x8d\x88\x8d"\x8d\x82\x8d\x8a\x0c\xf1'
            turfioTemps = tfioTempEq(int.from_bytes(data[0:2],byteorder='big'))
            
            surfHSTemps = []
            for iter in range(2,16,2): 
                surfHSTemps.append(hsTempEq(int.from_bytes(data[iter:iter+2],byteorder='big')))
            surfAPU = []
            surfRPU = []
            if times % 6 == 0 :
                hsk.send(HskPacket(tio, 'eEnable', data=[0x40, 0x40]))
                pkt = hsk.receive()
                for j in range(len(surf)):
                    val = (surf[j][1])
                    hsk.send(HskPacket(val, 'eTemps'))
                    data = hsk.receive().data

                    surfAPU.append(surfTempsEq(int.from_bytes(data[0:2],byteorder='big')))
                    surfRPU.append(surfTempsEq(int.from_bytes(data[2:4],byteorder='big')))

                    print(f'SURF Temps: {surfTempsEq(int.from_bytes(data[0:2],byteorder="big"))}')
                if len(surf) == 6: 
                    surfAPU.append(0)
                    surfRPU.append(0)
                if processors_off:
                    processorsOff(tio, surf)
            else:
                for j in range(len(surf)):
                    surfAPU.append(0)
                    surfRPU.append(0)
                if len(surf) == 6: 
                    surfAPU.append(0)
                    surfRPU.append(0)
            hsk.send(HskPacket(tio, 'eCurrents'))
            data = hsk.receive().data
            # data = b'\x03\xf5\x8c \x8c\x80\x8c\x88\x8c"\x8c\x82\x8c\x8a\x08\xed'
            turfioCurrent = tfioCurrentEq(int.from_bytes(data[0:2],byteorder='big'))
           
            surfCurrent = []
            for iter in range(2,16,2): 
                surfCurrent.append(surfCurrentEq(int.from_bytes(data[iter:iter+2],byteorder='big')))

            ts = time.time()
            new_data = [i,datetime.fromtimestamp(ts).strftime('%H:%M:%S'), turfioVolts, *surfVolts, turfioTemps, *surfHSTemps, *surfAPU, *surfRPU, turfioCurrent, *surfCurrent ]
            csv_writer.writerow(new_data)
        time.sleep(5)

            
