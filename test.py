import threading   , time,subprocess,signal
a=subprocess.Popen('pimpleFoam -case openfoam',shell=True) 
time.sleep(2)
print('aaa')
a.send_signal(signal.SIGSTOP)
print('bbb')
a.send_signal(signal.SIGCONT)
print('ccc')
