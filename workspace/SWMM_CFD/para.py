# ioControl



dir = '/home/jlong/workspace/SWMM_CFD/Case'
# timeControl
timeControl={'startTime':0,'endTime':5,'deltaT':0.5}
patch = {'time':0,'field':'U','boundary':['movingWall'],'timeStep':0.5}
# Cases
## SWMM
case0 = {'model':'SWMM','name':'swmm.inp','timeControl':timeControl,'Dir':dir,'timeStep':0.1}
case01 = {'model':'SWMM','name':'swmm1.inp','timeControl':timeControl,'Dir':dir,'timeStep':0.1}
## OpenFOAM
case1={'model':'OpenFOAM','name':'cavity','timeStep':0.02,'timeControl':timeControl,'Dir':dir,'patch':patch}
case2={'model':'OpenFOAM','name':'case2','timeStep':0.02,'timeControl':timeControl,'Dir':dir}

# Case input
# Sequence of cases running
cases = [case1]
