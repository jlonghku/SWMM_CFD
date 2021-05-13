from pyswmm import Simulation, Nodes
import time
sim= Simulation('/home/jlong/workspace/SWMM_CFD/swmm1.inp') 
for step in sim:
    print((sim.current_time-sim.start_time).total_seconds())

    time.sleep(1)
