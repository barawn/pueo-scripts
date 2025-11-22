from HskSerial import HskEthernet, HskPacket
import argparse
from pueo.turf import PueoTURF
from EventTester import EventServer
from startup.eventStartup import eventStartup

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--close",action="store_true")
    args = parser.parse_args()
    dev = PueoTURF()
    es = EventServer()

    #dev.trig.mask = 0xbffffff#201326591 # for just surf 26

    if(not args.close):
        es.open()
        dev.trig.runcmd(dev.trig.RUNCMD_RESET)
    else:
        es.close()
        dev.trig.runcmd(dev.trig.RUNCMD_STOP)
