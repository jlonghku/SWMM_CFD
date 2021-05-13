from pyswmm import Simulation

sim=Simulation('/home/jlong/work/SWMM_CFD/Case/SWMM/1.inp') 
for step in sim:
    print(sim.current_time)
