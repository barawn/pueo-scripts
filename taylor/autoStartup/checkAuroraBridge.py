from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF

dev = PueoTURF()

def bridgeCheck(): 
    dev = PueoTURF()
    down = []
    for i in range(0,4): 
        val = dev.aurora.linkstat(i)
        if val != 831: 
            down.append(i)
        
    if len(down) == 0: 
        return [4]
    else: 
        return down
    