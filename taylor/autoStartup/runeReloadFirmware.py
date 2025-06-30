from HskSerial import HskPacket

def runeReloadFirmware(hsk, port):

    # map of all turfios to ports for the turf
    tios = [ (0, 0x58), 
            (1, 0x50), 
            (2, 0x40), 
            (3, 0x48) ] 
    
    # if port is valid, reload firmware 
    for i in range(len(port)): 
        for tio in tios: 
            if port[i] == tio[0]: 
                hsk.send(HskPacket(tio[1], 'eReloadFirmware', data = [0,0,0,0]))
    