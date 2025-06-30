from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF

# Function to check if the bridge between the TURF and TURFIO
# is up
def bridgeCheck(): 
    
    # create TURF object
    dev = PueoTURF()
    
    # to hold all the down link port numbers
    down = []

    for i in range(0,4): 
        val = dev.aurora.linkstat(i)

    # a down link throws back 828. 831 is a successful bridge
        if val != 831: 
            down.append(i)
        
    # send back all down links if they are not up 
    # otherwise send 4 as a 'all good!'
    if len(down) != 0: 
        return down
    else: 
        return [4]
    