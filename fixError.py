import sys
from HskSerial import HskEthernet, HskPacket
import os
import time
import sys


def handle_error(code, tio=False, slot=False):

    # PMBus slot 
    # Use RACK addrs << 1
    # RACK addrs: 0x10, 0x40, 0x44, 0x11, 0x41, 0x45, 0x46
    pmbusslot = { 0 : 0x20 , 
             1 : 0x80 , 
             2 : 0x88 , 
             3 : 0x22 ,
             4 : 0x82 , 
             5 : 0x8a ,
             6 : 0x8c  }
       
    tios = { 0 : 0x58, 
            1 : 0x50 , 
            2 : 0x40 , 
            3 : 0x48 } 
    
    hsk = HskEthernet()
    if code == 1:
        print("Handling GTP link 0 error: Restarting GTP interface...")
        hsk.send(HskPacket(0x58, 'eReloadFirmware', data=[0,0,0,0]))
        time.sleep(5)
    elif code ==2: 
        print("Handling GTP link 1 error: Restarting GTP interface...")
        hsk.send(HskPacket(0x50, 'eReloadFirmware', data=[0,0,0,0]))
        time.sleep(5)
    elif code ==3: 
        print("Handling GTP link 2 error: Restarting GTP interface...")
        hsk.send(HskPacket(0x40, 'eReloadFirmware', data=[0,0,0,0]))
        time.sleep(5)
    elif code == 4: 
        print("Handling GTP link 3 error: Restarting GTP interface...")
        hsk.send(HskPacket(0x48, 'eReloadFirmware', data=[0,0,0,0]))
        time.sleep(5)
    elif code == 50: 
        print('Handling n')
        print(hex(tios[tio]))
        print(hex(pmbusslot[slot]))
        # hsk.send(HskPacket(hex(tios[tio]), 'ePMBus', data = [0x00, hex(pmbusslot[slot]), 0xD9]))
    elif code == 51: 
        print('Handling n')
        print(hex(tios[tio]))
        print(hex(pmbusslot[slot]))
        # hsk.send(HskPacket(hex(tios[tio]), 'ePMBus', data = [0x00, hex(pmbusslot[slot]), 0xD9]))
    elif code == 52: 
        print('Handling n')
        print(hex(tios[tio]))
        print(hex(pmbusslot[slot]))
        # hsk.send(HskPacket(hex(tios[tio]), 'ePMBus', data = [0x00, hex(pmbusslot[slot]), 0xD9]))
    elif code == 99:
        print("What just happened...")
    elif code==100: 
        # from Payton's startup script (thank youuuuu)
        
        print('Rebooting the TURF now. This will take ~60 seconds.')

        ## First thing is we are going to reset CPU and reboot the TURF
        os.system('/home/pueo/pueo-scripts/taylor/ppython /home/pueo/pueo-scripts/ftdi-turf-restart.py --cpu')
        time.sleep(60)
    else:
        print(f"Unknown error code: {code}. No action taken.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 fix_error.py <error_code>")
        sys.exit(1)
    try:
        error_code = int(sys.argv[1])
        handle_error(error_code)
        time.sleep(5)
    except ValueError:
        print("Error: Invalid error code. Must be an integer.")
        sys.exit(1)
