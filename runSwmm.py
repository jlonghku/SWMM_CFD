from pyswmm import Simulation, Nodes
import iodata,signal
import threading,os,para,subprocess,checkstate as ck

dirs=para.dirs

with Simulation('./1.inp') as sim:
        node_object = Nodes(sim)  
        for step in sim:
            #print(sim.current_time)
            k=sim.current_time-sim.start_time
            print(k.total_seconds())
            #node_object['01'].generated_inflow(iodata.read_data("data.out"))
            # print(node_object['01'].total_outflow)
            with open("data.in",'w') as f1:
                    f1.writelines(str(node_object['01'].total_outflow))
                
