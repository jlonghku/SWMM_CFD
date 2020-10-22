
import iodata,signal,isRun as isr,time
import threading,os,para,subprocess,checkState as ck,getOfTime as got

dirs=para.dirs
con = threading.Condition()
con1[0]=threading.Condition()
of_time=0
sw_time=0
init=para.init

class runSwmm(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global sw_time,of_time,init
        from pyswmm import Simulation, Nodes
        dirs=para.dirs
        con.acquire()
        with Simulation('./1.inp') as sim:
                node_object = Nodes(sim)  
                for step in sim:                   
                        sw_time=(sim.current_time-sim.start_time).total_seconds()/6000
                        print(sw_time)
                        with open("data.in",'w') as f1:
                                f1.writelines(str(node_object['01'].total_outflow))
                        if not os.path.exists(dirs):
                                os.mkdir(dirs)
                        os.system("""awk -F"[()]" 'NR>1{print "("$2")" " (0 0 0) 1"}' """+"""data2.out > comms/data2.in""")
                        if isr.isRun(dirs,init,sw_time,of_time)==2:
                                os.system('touch '+dirs+'OpenFOAM.lock')
                                con.notify()  
                                # wait message
                                con.wait()
        # release the lock
        con.release()

class runOpenfoam(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global of_time,sw_time,init
        # get lock
        con.acquire()
        of_case=subprocess.Popen('pimpleFoam -case openfoam',shell=True) 
        while True:
                of_time=got.getOfTime(dirs)
                m=isr.isRun(dirs,init,sw_time,of_time)
                if isr.isRun(dirs,init,sw_time,of_time)==1 :
                        of_case.send_signal(signal.SIGSTOP)
                        # 唤醒等待的线程
                        con.notify()  
                        # 等待通知
                        con.wait()
                        of_case.send_signal(signal.SIGCONT)
                elif isr.isRun(dirs,init,sw_time,of_time)==2:
                        os.system("""awk -F"[()]" 'NR>1{print "("$2")" " (0 0 0) 1"}' """+dirs+"""data2.out > comms/data2.in""")
                        os.system('touch '+dirs+'OpenFOAM.lock')
        # 释放锁
        con.release()

os.system('python3 pre_swof.py')
of =runOpenfoam()
sw =runSwmm()
if (init==0):            
        of.start()
        sw.start()
else:
        sw.start()
        of.start()

