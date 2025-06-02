from EventTester import EventServer
from pueo.turf import PueoTURF

def eventStartup():
    # n.b. enable the SURF datapath outside of this!!
    # Need to check that the event stuff only runs between
    # RUN_RESET/RUN_STOP.
    
    es = EventServer()
    dev = PueoTURF()
    
    # reset event
    dev.event.reset()
    
    # only 2 TURFIOs for me
    # 1 = drop all data from this TURFIO
    dev.event.mask = 0b1100
    
    # latency from now -> trigger readout (time for triggers to arrive)
    # this is probably waaay short
    dev.trig.latency = 200
    
    # this is the lookback time from all triggers. It should be
    # the RF trigger latency/8 ns - (512/24). This is because
    # you want to go forward 512 samples after the trigger, and
    # this is a negative offset. This is in units of 24 samples
    # hence the divide by 24. This is actually a signed 12-bit
    # integer, but has range of a signed 16-bit integer.
    dev.trig.offset = 0
    
    # open the event path.
    es.open()
    
    print("Statistics at start:")
    st = dev.event.statistics(verbose=True)
    
    # start it up, baby
    dev.trig.runcmd(dev.trig.RUNCMD_RESET)

    return (dev, es)

