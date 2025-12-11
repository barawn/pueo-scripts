from pueo.turf import PueoTURF
from pueo.turfio import PueoTURFIO
from pueo.surf import PueoSURF
import csv

dev = PueoTURF()
filename="check1.csv"
with open(filename, 'w', newline='') as csvfile:
    csv_writer=csv.writer(csvfile)
    for i in range(4):
        tio = PueoTURFIO((dev,i), 'TURFGTP') 
        if i == 0 or i == 1: 
            for j in range(7): 
                surf = PueoSURF((tio, j), 'TURFIO')
                identity=f"v0r{surf.identify()['DateVersion'].minor}p{surf.identify()['DateVersion'].rev}"
                trigconfig=hex(surf.trigger_config & 0xFF00)
                new_data=[i,j,identity,trigconfig]
                csv_writer.writerow(new_data)
        else: 
            for j in range(6): 
                surf = PueoSURF((tio, j), 'TURFIO')
                identity=f"v0r{surf.identify()['DateVersion'].minor}p{surf.identify()['DateVersion'].rev}"
                trigconfig=hex(surf.trigger_config & 0xFF00)
                new_data=[i,j,identity,trigconfig]
                csv_writer.writerow(new_data)

