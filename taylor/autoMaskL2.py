from pueo.turf import PueoTURF
import argparse

parser = argparse.ArgumentParser()


parser.add_argument("--trigrate", type=int) # L2 trigger rate 
parser.add_argument("--removesurf",  type=str) # manually removing SURFs 
args = parser.parse_args()

# Make list of all SURFs you wanna remove manually
if not args.removesurf:
    removed  =[]
else: 
    removed = list(map(int,args.removesurf.split(',')))


dev = PueoTURF()
premask = dev.trig.mask # get the initial mask 

print(f'Before: {bin(premask)}') # debug output 

l1surfs = dev.trig.scaler.scalers() # L1 scalers as seen by TURF
l2surfs = dev.trig.scaler.leveltwos() # L2 scalers as seen by TURF 

l2rate = sum(l2surfs) # get the overall rate of L2 trigs 
print(f'Reported L2 Triggers: {l2rate}')

# LUT form { L2_idx, [[L1_idx above,actual,below], [data_idx above,actual,below]]}
# this is super confusing 
L2Triggers = { 
            0 : [ [ 4, 5, 13 ] , [ 4, 5, 12 ]], 
            1 : [ [ 3, 4, 5 ] [ 3, 4, 5 ]], 
            2 : [ [ 2, 3, 4 ],  [ 2, 3, 4 ]], 
            3 : [ [1, 2, 3 ], [ 1, 2, 3 ]], 
            4 : [ [0, 1,2] [ 0, 1, 2 ]], 
            5 : [ [8, 0, 1], [ 7, 0, 1 ]], 
            6 : [ [9,8,0], [ 8, 7, 0 ]], 
            7 : [ [10,9,8] [ 9, 8, 7 ]], 
            8 : [ [11,10,9], [ 10, 9, 8 ]], 
            9 : [ [12,11,10], [ 11, 10, 9 ]], 
            10 : [ [13,12,11], [ 12, 11, 10]], 
            11 : [ [5,13,12], [ 5, 12, 11 ]], 
            12 : [ [28,29,21], [ 25, 26, 19 ]], 
            13 : [ [27,28,29] [ 24, 25, 26 ]], 
            14 : [ [26,27,28], [ 23, 24, 25 ]], 
            15 : [ [25, 26,27],  [ 22, 23, 24 ]], 
            16 : [ [24,25,26], [ 21, 22, 23 ]], 
            17 : [ [16,24,25], [ 14, 21, 22 ]], 
            18 : [ [17,16,24], [ 15, 14, 21 ]], 
            19 : [ [18,17,16], [ 16, 15, 14 ]], 
            20 : [ [19,18,17], [ 17, 16, 15 ]], 
            21 : [ [20,19,18], [ 18, 17, 16 ]], 
            22 : [ [21,20,19], [ 19, 18, 17 ]], 
            23 : [ [29,21,20] [ 26, 19, 18 ]]}


# create array to hold masked off SURFs 
maskoff = []

# check is the rate is higher than the L2 trigger rate 
if l2rate >= args.trigrate: 

    # if yes, find which SURF is being the annoying one 
    maxVal = max(l2surfs)

    # grab the L2 trigger idx of max sector 
    maxIndex = l2surfs.index(maxVal)
    L1Trigger, SURFdata = L2Triggers[maxIndex][0], L2Triggers[maxIndex][1]

    maxIndex = max(L1Trigger, key=lambda i: l1surfs[i]) # gives index in array 
    # matches to the index of surf in data array 
    maxL1Trig = l1surfs[maxIndex] # solely for printout

    print(f'Max L1 trigger found: {maxL1Trig}, gotta mask that off')
    maskoff.append(maxIndex)

    
"""for i in range(len(l1surfs)):
    if l1surfs[i] >= args.trigrate:
        print(f'SURF {i} firing too fast!')
        maskoff.append(i)
if maskoff: 
    print('Masking off!')"""


for remove in removed:
    premask |= (1 << remove) # this is to remove surfs manually 


# for j in range(len(maskoff)):
premask |= (1 << SURFdata[maxIndex])

for k in range(27):
    if k not in maskoff and k not in removed:
        premask &= ~(1 << k)

print(f'After: {bin(premask)}')

dev.trig.mask = premask

