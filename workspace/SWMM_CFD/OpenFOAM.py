
import os
import subprocess
import tools as tl


class case(object):
    def __init__(self, inp):
        # data to create a case, include parameters:
        # name: folder name of the case
        # path: path of the case
        # comdir: dir for data exchange
        self.dict = inp
        # pre-processing
        self.modifyBoundary()
        self.load(self.get('timeControl'))
        subprocess.Popen(
            "/home/jlong/workspace/SWMM_CFD/preOpenFOAM.sh " + self.get('path'), shell=True)

    def load(self, dict):
        for k, v in dict.items():
            os.system('foamDictionary %s/system/controlDict -entry %s  -set %g' %
                      (self.get('path'), k, v))

    def get(self, info):
        return self.dict.get(info)

    def start(self):
        # first run
        subprocess.Popen(
            "/home/jlong/workspace/SWMM_CFD/runOpenFOAM.sh " + self.get('path'), shell=True)

    def continueRun(self):
        os.system("touch " + self.get('comDir') + "/OpenFOAM_" + self.get('name') +
                  ".lock")

    def isRun(self):
        return os.path.exists(self.get('comDir') + "/OpenFOAM_" + self.get('name') +
                              ".lock")

    def time(self):
        return tl.readTime(self.get('path')+'/postProcessing/time/0/time.dat')

    def modifyBoundary(self):
        os.system(
            'foamDictionary %s/system/controlDict -entry libs -merge \\( "libcustomfiniteVolume.so" \\)' % self.get('path'))
        # set coupled boundary condition
        self.patchDict = self.get('patch')
        for pi in self.patchDict.get('boundary'):
            os.system("""foamDictionary %s/%s/%s -entry boundaryField.%s -set '
                        {
                            type            externalCoupledNew;
                            commsDir        "/home/jlong/workspace/SWMM_CFD/Case/comms";
                            waitInterval    0;
                            //calcFrequency   1;
                            calcInterval    %s;
                            file            data_%s_%s;
                            initByExternal  0;
                        }'""" % (self.get('path'), self.patchDict.get('time'), self.patchDict.get('field'), pi, self.patchDict.get('timeStep'), 'OpenFOAM', self.get('name')))
        os.system("createExternalCoupledPatchGeometryNew -case " +
                  self.get('path')+" U")

    def updateBoundary(self):
        # update boundary
        mapcmd = "mapPatch -v -toFiles \( " + self.get('comDir') + " patchPoints_OpenFOAM_" + self.get(
            'name') + " patchFaces_OpenFOAM_" + self.get('name') + " data_OpenFOAM_" + self.get('name') + ".in \)   "
        mapcmd += "-fromFiles \( " + self.get('comDir') + " patchPoints_OpenFOAM_" + self.get('name') + \
            " patchFaces_OpenFOAM_" + \
            self.get('name') + " data_OpenFOAM_" + self.get('name') + ".out \)"
        
        os.system(mapcmd)
