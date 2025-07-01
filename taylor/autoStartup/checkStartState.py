from HskSerial import HskEthernet, HskPacket
import signal
from time import sleep    # only needed for testing

timelimit_seconds = 3    # Must be an integer

# Custom exception for the timeout
class TimeoutException(Exception):
    pass

# Handler function to be called when SIGALRM is received
def sigalrm_handler(signum, frame):
    # We get signal!
    raise TimeoutException()


def checkStartState(hsk): 
    #hsk = HskEthernet()
    tio0 = (0, 0x58)
    surf0 = [ (0, 0x97),
            (1, 0xa0),
            (2, 0x99),
            (3, 0x8d),
            (4, 0x9d),
            (5, 0x94),
            (6, 0x8a) ]

    tio1 = (1, 0x50)
    surf1 = [ (0, 0x8c),
            (1, 0x95),
            (2, 0x9f),
            (3, 0x9a),
            (4, 0x87),
            (5, 0x85), 
            (6, 0x9c)]

    tio2 = (2, 0x40)
    surf2 = [ (0, 0x89),
            (1, 0x88),
            (2, 0x9e),
            (3, 0x8b),
            (4, 0xa1),
            (5, 0x98)]

    tio3 = (3, 0x48)
    surf3 = [ (0, 0x93),
            (1, 0x9b),
            (2, 0x96),
            (3, 0x8e),
            (4, 0x90),
            (5, 0x92) ]
    
    tios = [tio0, tio1, tio2, tio3]
    surfs = [surf0, surf1, surf2, surf3]

    failed = []
    for tio in tios: 
        hsk.send(HskPacket(tio[1], 'eEnable', data = [0x40, 0x40]))
        pkt = hsk.receive()
        idx = tios.index(tio)
        for surf in surfs[idx]:
            pkt = 0 
            hsk.send(HskPacket(surf[1], 'eStartState'))
            # Set up signal handler for SIGALRM, saving previous value
            old_handler = signal.signal(signal.SIGALRM, sigalrm_handler)
            # Start timer
            signal.alarm(timelimit_seconds)
            try:
                pkt = hsk.receive().data
                #if pkt is None:
                #    failed.append((tio[1], surf[0]))
                #    print('failed to receive a response')
            except TimeoutException: 
                #print(pkt) 
                print('failed to receive a response within the time limit...')
                failed.append((tio[1], surf[0]))
                #print('all good yo :D')
                continue 
            finally:
                # Turn off timer
                signal.alarm(0)
                # Restore handler to previous value
                signal.signal(signal.SIGALRM, old_handler)
    if (len(failed) == 0):
        return 0
    else:
        return failed
    

#checkStartState(1)