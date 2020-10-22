from pyswmm import Simulation, Nodes,Links
i=0
with Simulation('1.inp') as sim:
        for step in sim:
                i=i+1
                print(i) 
                pass
        print('finish')


