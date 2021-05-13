a=0
print((a!=0)*2)
while True:
    continue
    print(a)
    a+=1
    if a==10000:
        break

    mapPatch -v -fromFiles \( \( . patchPoints patchFaces *.out \) \) -toFiles \( . patchPoints patchFaces data_U_oo.in \)