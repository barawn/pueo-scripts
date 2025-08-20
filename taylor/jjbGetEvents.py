import time
from pueo.turf import PueoTURF
from EventTester import EventServer
import pickle
import datetime
import subprocess

# File
now = datetime.datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
outfile="surfdata"+formatted_time+".pkl"
countfile="surfcounts"+formatted_time+".txt"
bfile="surflevel"+formatted_time+".txt"
outfile=outfile.replace(" ","_")
countfile=countfile.replace(" ","_")
outfile=outfile.replace(":","-")
countfile=countfile.replace(":","-")
bfile=bfile.replace(":","-")
print(f"Writing to files {outfile}, {countfile}, and {bfile}")
#
dev=PueoTURF()
es=EventServer()
dev.trig.mask = 0xC0FFFFFF #unmask TURFIO 3 slots 5 and 6 for now
dev.trig.offset = 36
runtime=15.0
es.open()
dev.trig.runcmd(dev.trig.RUNCMD_RESET)
time.sleep(1)
start_time=time.time()
start_ccount=dev.event.completion_count
start_tcount=dev.trig.trigger_count
print(f"Starting Completion Count:{start_ccount}")
print(f"Starting Trigger Count:{start_tcount}")
count=0
e=[]
while time.time() - start_time < runtime: #run for runtime seconds
    #grab one event here
    while (dev.event.completion_count == 0):
        pass
    e.append(es.event_receive())
    count += 1
#close out here
es.close()
dev.trig.runcmd(dev.trig.RUNCMD_STOP)
end_ccount=dev.event.completion_count
end_tcount=dev.trig.trigger_count
print(f"Events Collected:{count}")
print(f"Ending  Completion Count:{end_ccount}")
print(f"Ending Trigger Count:{end_tcount}")
#print("Event Rate is ", count/runtime, "\n")
f = open(outfile, 'wb') 
pickle.dump(e,f)
f.close()
cf = open(countfile, 'w') 
print(f"Starting Completion Count:{start_ccount}",file=cf)
print(f"Starting Trigger Count:{start_tcount}",file=cf)
print(f"Events Collected:{count}",file=cf)
print(f"Ending  Completion Count:{end_ccount}",file=cf)
print(f"Ending Trigger Count:{end_tcount}",file=cf)
cf.close()
# levelCheckCmd=["taylor/ppython","taylor/beamLevelCheckAll.py","--tio","3","--slots","4,5"]
# bresult=subprocess.run(levelCheckCmd, stdout=subprocess.PIPE)
# bf = open(bfile, 'w')
# bf.write(bresult.stdout)
# bf.close()
print("Compressing output with zstd:")
command = ["zstd","--rm",outfile ] 
# Execute the command and direct its output to the terminal
# capture_output=False ensures output is not captured by Python, but sent to stdout/stderr
# text=True decodes stdout/stderr as text using default encoding
result = subprocess.run(command) 
# You can optionally check the return code to see if the command was successful
if result.returncode == 0:
    print("zstd executed successfully.")
else:
    print(f"zstd failed with exit code: {result.returncode}")
