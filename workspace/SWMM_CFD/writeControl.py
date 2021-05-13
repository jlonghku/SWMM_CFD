import os
root = '/home/jlong/workspace/SWMM_CFD/Case/OpenFOAM'
#root = '.'
case = 'cavity'
time = 0
field = 'U'
timestep = 0.03
patch = ['movingWall']
os.system('sudo chmod 777 -R ' + root)

# # enable functions
# os.system(
#     'foamDictionary %s/%s/system/controlDict -entry functions  -merge {}' %
#     (root, case))
# # change timesteps
# os.system(
#     """foamDictionary %s/%s/system/controlDict -entry functions.uniTimeStep -set '''       
#             {
#                 type            coded;
#                 libs            ( "libutilityFunctionObjects.so" );
#                 name            setTimeSetp;
#                 writeControl    adjustableRunTime;
#                 writeInterval   %s;
#                 executeControl  timeStep;
#                 executeInterval 1;
#                 codeInclude     #{
#                     //#include "/home/jlong/backup/inp_new/WASP.H"                 
#                 #};    
#                 codeData        #{                        
#                     scalar ccccc=5;                
#                 #};      
#                 codeExecute     #{     
#                     #include "/home/jlong/backup/inp_new/uniTimeStep.H"
#                 #};            
#             }'''""" % (root, case, timestep))

# enable newPatch
os.system(
    'foamDictionary %s/%s/system/controlDict -entry libs -merge \\( "libcustomfiniteVolume.so" \\)'
    % (root, case))
# set coupled boundary condition
for pi in patch:
    os.system("""foamDictionary %s/%s/%s/%s -entry boundaryField.%s -set '
                {
                    type            externalCoupledNew;
                    commsDir        "/home/jlong/workspace/SWMM_CFD/Case/comms";
                    waitInterval    0;
                    //calcFrequency   1;
                    calcInterval    %s;
                    file            data_%s_%s;
                    initByExternal  0;
                }'""" % (root, case, time, field, pi,timestep, field, case))
