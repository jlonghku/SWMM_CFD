import os, subprocess,signal,threading,sys
#of_case=subprocess.Popen('cd /home/jlong/OFcase/wave&&mpirun -np 8 interFoam -parallel',shell=True) 
#sw_case=subprocess.Popen('cd /home/jlong/OFcase/cavity&&mpirun -np 8 icoFoam -parallel',shell=True) 
#_thread.start_new_thread(subprocess.Popen,('mpirun', '-np', '8' ,'interFoam' ,'-parallel'))
#of_case.send_signal(signal.SIGSTOP)
#of_case.send_signal(signal.SIGINT)
#sw_case.start()
#of_case.send_signal(signal.SIGINT)
class mypopen(threading.Thread):
    def  __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print("c")
        of_case=subprocess.Popen('cd /home/jlong/OFcase/wave&&mpirun -np 8 interFoam -parallel',shell=True)

mm=mypopen()
mm.start()

def signal_handler(signal, frame):
    sys.exit(0)
 
signal.signal(signal.SIGINT,signal_handler)
while True:
   pass
