import os, time,para,subprocess,checkstate as ck

dirs=para.dirs
#os.system('touch '+dirs+'OpenFOAM.lock')
subprocess.Popen('pimpleFoam -case openfoam',shell=True) 


while (1):
    #para.islock,para.isout=ck.checkstate(para.dirs)

    os.system('foamListTimes -case openfoam >of_timelist.log')
    with open("of_timelist.log") as f:
        lines=f.readlines()
        latest_time=float(lines[-1])
    if (para.islock==False)&(para.isout==True)&(latest_time<0.04):
        os.system("""awk -F"[()]" 'NR>1{print "("$2")" " (0 0 0) 1"}' """+dirs+"""data2.out > comms/data2.in""")
        os.system('touch '+dirs+'OpenFOAM.lock')
    elif (para.islock==False)&(para.isout==True)&(latest_time>=0.04):
        print(111)
        os.system("""awk -F"[()]" 'NR>1{print "("$2")" " (0 0 0) 1"}' """+dirs+"""data2.out > comms/data2.in""")
        os.system('touch '+dirs+'OpenFOAM.lock')
        #time.sleep(1)


