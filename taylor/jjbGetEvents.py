import time
from pueo.turf import PueoTURF
from EventTester import EventServer
import pickle

dev=PueoTURF()
es=EventServer()
dev.trig.mask = 0xC0FFFFFF #unmask TURFIO 3 slots 5 and 6 for now
dev.trig.offset = 36
es.open()
dev.trig.runcmd(dev.trig.RUNCMD_RESET)
time.sleep(1)
start_time=time.time()
ccount=dev.event.completion_count
print(f"Completion Count:{ccount}")
count=0
e=[]
while time.time() - start_time < 5.0: #run for five seconds
    #grab one event here
    while (dev.event.completion_count == 0):
        pass
    e.append(es.event_receive())
    count += 1
#close out here
es.close()
dev.trig.runcmd(dev.trig.RUNCMD_STOP)
print("Event Rate is ", count/5, "\n")
f = open('jjbevents.pkl', 'wb') 
pickle.dump(e,f)
f.close()
