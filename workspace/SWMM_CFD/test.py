
import signal,os
import subprocess
of_case=subprocess.Popen('mpirun -np 6 pimpleFoam -case openfoam',shell=True) 
while(1):  
    if (os.path.isfile('./comms/data2.out')&(not os.path.isfile('./comms/OpenFOAM.lock'))):
        of_case.send_signal(signal.SIGSTOP)
        os.system('mapPatch -v -fromFiles  \( \( comms patchPoints patchFaces data2.out \) \) -toFiles \( comms patchPoints patchFaces data2.in \) >/dev/null 2>&1')
        os.system('touch '+'./comms/OpenFOAM.lock')      
        of_case.send_signal(signal.SIGCONT)     
    if ((not os.path.isfile('./comms/OpenFOAM.lock'))&os.path.isfile('./comms/data.out')):
        of_case.send_signal(signal.SIGSTOP)
        os.system('mapPatch -s -case comms >/dev/null 2>&1')
        os.system('touch '+'./comms/OpenFOAM.lock')
        of_case.send_signal(signal.SIGCONT)
        case[0].send_signal(signal.SIGSTOP)