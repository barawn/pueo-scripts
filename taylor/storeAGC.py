import time
import pickle
from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF

dev =PueoTURF()
tio=PueoTURFIO((dev,3),'TURFGTP')
surf4=PueoSURF((tio,4),'TURFIO')
surf5=PueoSURF((tio,5),'TURFIO')
alltime=[]
starttime=time.time()
count=0
while (time.time()-starttime < 1.): #run for 1. second
    startthis=time.time()
    thistime=[]
    for i in range(8): #loop over channels 
        #sqr4=surf4.levelone.read(0x4004+0x400*i)/65536
        #gt4=surf4.levelone.read(0x4008+0x400*i)/65536
        #lt4=surf4.levelone.read(0x400c+0x400*i)/65536
        #scale4=surf4.levelone.read(0x4010+0x400*i)
        #offset4=surf4.levelone.read(0x4014+0x400*i)
        #done5=surf5.levelone.read(0x4000+0x4004*i)
        sqr5=surf5.levelone.read(0x4004+0x400*i)/65536
        gt5=surf5.levelone.read(0x4008+0x400*i)/65536
        lt5=surf5.levelone.read(0x400c+0x400*i)/65536
        scale5=surf5.levelone.read(0x4010+0x400*i)
        offset5=surf5.levelone.read(0x4014+0x400*i)
        thistime.append([sqr5,gt5,lt5,scale5,offset5])
    alltime.append(thistime)
    count += 1
    while (time.time()-startthis < 174.76e-6):
        pass
print("Count:",count)
f = open('jjbAGC.pkl', 'wb')
pickle.dump(alltime,f)
f.close()   #print(f"Ch {i:2} Var:{sqr:11.3e} GT:{gt:11.3e} LT:{lt:11.3e} Scale:{scale:11d} Offset:{offset:11d}")
