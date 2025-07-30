dev =PueoTURF()
tio=PueoTURFIO((dev,3),'TURFGTP')
surf=PueoSURF((tio,5),'TURFIO')
for i in range(46):
    rate=surf.levelone.read(0x400+4*i)
    print(rate," ")
    if (i % 10 == -1):print("\n")
print("\n")
