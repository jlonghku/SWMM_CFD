from pyswmm import Simulation, Nodes
import time
import threading, datetime
sim1 = '/home/jlong/workspace/SWMM_CFD/swmm.inp'
sim = '/home/jlong/workspace/SWMM_CFD/swmm1.inp'


class tt(threading.Thread):
    def __init__(self, dir):
        # start threading
        threading.Thread.__init__(self)
        self.dir = dir

    def run(self):
        self.sim = Simulation(self.dir)
        self.sim.start_time = self.sim.start_time + datetime.timedelta(
            seconds=120)
        self.sim.end_time = self.sim.start_time + datetime.timedelta(
            seconds=360)
        for step in self.sim:
            print(self.sim.current_time)
        self.sim.report()
        self.sim.close()


a = tt(sim)
b = tt(sim1)
a.start()

b.start()
a.join()
b.join()
