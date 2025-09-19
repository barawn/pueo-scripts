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
    
    surfsTio0 = { 0 : 0x97 , 
             1 : 0xa0 , 
             2 : 0x99 , 
             3 : 0x8d ,
             4 : 0x9d ,
             5 : 0x94 ,
             6 : 0x8a  }
    
    surfsTio1 = { 0 : 0x8c , 
             1 : 0x95 , 
             2 : 0x9f , 
             3 : 0x9a ,
             4 : 0x87 , 
             5 : 0x85 ,
             6 : 0x91 }

    surfsTio2 = { 0 : 0x89 , 
             1 : 0x88 , 
             2 : 0x9e , 
             3 : 0x8b ,
             4 : 0xa1 , 
             5 : 0x98  }
    
    surfsTio3 = { 0 : 0x93 , 
             1 : 0x9b , 
             2 : 0x86 , 
             3 : 0x8e ,
             4 : 0x90 , 
             5 : 0x92  }
    
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
        
        
        selectedTurfio = (tios[tio])
        selectedPMBusAddr = (pmbusslot[slot])
        
        # stolen from paytons code
        hsk.send(HskPacket(selectedTurfio, 'eCurrents'))
        data = hsk.receive().data
        currents = []
        """ for iter in range(1, 16, 2):
            val = (int.from_bytes(data[iter:iter+2], byteorder='big') )
            
            I = (val - 2048)*12.51/4.762
            # lets add tiers :D
            if I < 0 or I > 1000: 
                # either hotswap has died or TURFIO is refusing to admit that that is there 
                hsk.send(HskPacket(selectedTurfio, 'eReloadFirmware', data=[0,0,0,0]))
                pkt = hsk.receive()
            elif I > 0 and I < 500 : 
                # yea that SURF isn't booted right 

                """
            
        hsk.send(HskPacket(selectedTurfio, 'eEnable', data=[0x40, 0x40]))
        pkt = hsk.receive() # to receive the packet 
        print(f'Sending ePMBus to power cycle SURF (TIO {hex(selectedTurfio)}: RACK Addr {hex(selectedPMBusAddr)})')
        hsk.send(HskPacket(selectedTurfio, 'ePMBus', data = [0x00, selectedPMBusAddr, 0xD9]))
        pkt = hsk.receive()
        time.sleep(25) # 20s worked lets try less?
        

    elif code == 51: 
        print('Sending eRestart')
        selectedTurfio = (tios[tio])
        if tio == 0: 
            selectedSurf = surfsTio0[slot]
        elif tio == 1: 
            selectedSurf = surfsTio1[slot]
        elif tio == 2: 
            selectedSurf = surfsTio2[slot]
        elif tio == 3: 
            selectedSurf = surfsTio3[slot]
        hsk.send(HskPacket(selectedTurfio, 'eEnable', data = [0x40, 0x40]))
        pkt = hsk.receive()
        time.sleep(1) 
        hsk.send(HskPacket(selectedSurf, 'eRestart', data = [0]))
        time.sleep(5)

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
