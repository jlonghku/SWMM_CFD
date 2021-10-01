import os
import subprocess
import tools as tl
import threading
import numpy as np


class case(threading.Thread):
    def __init__(self, inp):
        # construct a new case (essential function)
        threading.Thread.__init__(self)
        # data to create a case, include parameters:
        self.dict = inp

        # pre-processing
        ## setup path and filenames
        self.name_ = self.dict["name"]
        self.path_ = self.dict["path"]
        self.comDir_ = self.dict["comDir"]
        self.lockFile_ = self.comDir_ + "/OpenFOAM_" + self.name_ + ".lock"

        ## setup time
        self.startTime_ = self.dict["timeControl"]["startTime"]
        self.time_ = self.startTime_
        self.endTime_ = self.dict["timeControl"]["endTime"]
        self.timeStep_ = self.dict["timeControl"]["timeStep"]
        self.loadTime(self.dict["timeControl"])
        ## clean postProcessing dir for time record
        tl.cleanDir("%s/postProcessing/time/%s" % (self.path_, self.time_))
        self.timeFile_ = "%s/time.log" % self.path_

        ## setup boundary
        self.boundary_ = self.dict["boundaryControl"]
        self.modifyBoundary()
        self.outFile_ = {
            k: self.comDir_ + "/data_OpenFOAM_" + self.name_ + "_" + k + ".out"
            for k in set([v[1] for v in self.boundary_])
        }

    def loadTime(self, dict):
        os.system(
            "foamDictionary %s/system/controlDict -entry %s  -set %g >/dev/null"
            % (self.path_, "startTime", dict["startTime"])
        )
        os.system(
            "foamDictionary %s/system/controlDict -entry %s  -set %g >/dev/null"
            % (self.path_, "endTime", dict["endTime"])
        )
        os.system(
            "foamDictionary %s/system/controlDict -entry %s  -set %g >/dev/null"
            % (self.path_, "writeInterval", dict["timeStep"])
        )

    def run(self):
        # loop for OpenFOAM simulation (essential function)
        ## first run
        first = True
        ## run
        while self.time() < self.endTime_:
            self.con_child.acquire()
            if first:
                subprocess.Popen(
                    [
                        os.path.dirname(os.path.realpath(__file__)) + "/runOpenFOAM.sh",
                        self.path_,
                    ],
                    stdout=subprocess.DEVNULL,
                )
                first = False
            else:
                self.continueRun()
            self.wait()
            self.update()
            print("OpenFOAM-%s time: " % self.dict["name"])
            print(self.time())
            self.con_father.release()

    def getSem(self, father, child):
        # setup Semaphore for father and child threads to sync data (essential function)
        self.con_child = child
        self.con_father = father

    def continueRun(self):
        # restart OpenFOAM solver
        os.system("touch " + self.lockFile_)

    def isWait(self):
        # check the running state of OpenFOAM solver
        isRun = os.path.exists(self.lockFile_)
        isOut = False
        for v in self.outFile_.values():
            isOut = isOut or os.path.exists(v)
        self.updateTime()
        isStop = self.time_ == self.endTime_
        return isRun or not (isStop or isOut)

    def wait(self):
        # wait for solver stopping
        while self.isWait():
            pass

    def time(self):
        # return time
        return self.time_

    def update(self):
        # update time and boundary data
        self.updateTime()
        self.updateBoundary()

    def updateTime(self):
        # update time
        self.time_ = tl.readTime_OpenFOAM(self.timeFile_)

    def updateBoundary(self):
        # update boundary
        if self.time_ < self.endTime_:
            for v in self.outFile_.values():
                if os.path.exists(v):
                    b = tl.readBoundary_OpenFOAM(v)
                    for v1 in b:
                        for v2 in self.boundary_:
                            if v1[0] == v2[1] and v1[1] == v2[2]:
                                v2[3].update(v1[2])

    def boundary(self):
        return self.boundary_

    def setBoundary(self, boundary):
        # get boundary conditions from father thread (essential function)
        self.boundary_ = boundary
        self.transferBoundary()
        self.loadBoundary()

    def transferBoundary(self):
        # format the boundary value
        for v in self.boundary_:
            if v[3].get("model", 0) == "SWMM":
                if v[3].get("value_OpenFOAM", False):
                    magSfs = v[3]["magSf_OpenFOAM"]
                    values = v[3]["value_OpenFOAM"]
                    snGrads = v[3]["snGrad_OpenFOAM"]
                    Sfs = v[3]["Sf_OpenFOAM"]
                    val = 0
                    if isinstance(values[0], tuple):
                        for j in range(len(values)):
                            val += np.dot(values[j], Sfs[j])
                    else:
                        for j in range(len(values)):
                            val += magSfs[j] * values[j]
                    if val != 0:
                        v[3]["value_OpenFOAM"] = [
                            i * v[3]["value_SWMM"] / val for i in values
                        ]

    def loadBoundary(self):
        for k, v in self.outFile_.items():
            if os.path.exists(v):
                fieldType = tl.writeBoundary_OpenFOAM(self.boundary_, k, v)

                bcFiles = (
                    self.comDir_
                    + " patchPoints_OpenFOAM_"
                    + self.name_
                    + "_"
                    + k
                    + " patchFaces_OpenFOAM_"
                    + self.name_
                    + "_"
                    + k
                    + " data_OpenFOAM_"
                    + self.name_
                    + "_"
                    + k
                )

                mapcmd = (
                    "mapPatch -"
                    + fieldType
                    + " -toFiles \( "
                    + bcFiles
                    + ".in \) -fromFiles \( "
                    + bcFiles
                    + ".out \)"
                )

                subprocess.call(mapcmd, shell=True, stdout=subprocess.DEVNULL)
                # os.system(mapcmd)

    def modifyBoundary(self):
        # modify boundary parameters in openfoam inp file
        os.system(
            'foamDictionary %s/system/controlDict -entry libs -merge \\( "libcustomfiniteVolume.so" \\)'
            % self.path_
        )
        os.system(
            "foamDictionary %s/system/controlDict -entry functions -merge {}"
            % self.path_
        )
        subprocess.call(
            [
                "foamDictionary",
                "%s/system/controlDict" % self.path_,
                "-entry",
                "functions.time",
                "-merge",
                """{
        type            coded;
        libs            ( "libutilityFunctionObjects.so" );
        name            writeTime;
        writeControl    timeStep;
        writeInterval   1;
        code            #{
        #};
        codeExecute     #{
            const Time& runTime = mesh().time();        
            OFstream out("%s/time.log");
            out<<runTime.value()<<" "<<runTime.deltaTValue();
        #};
    }"""
                % self.path_,
            ],
            stdout=subprocess.DEVNULL,
        )
        tl.resetOpenFOAM("%s/%s" % (self.path_, self.startTime_))
        ## set coupled boundary condition
        for v in self.boundary_:
            subprocess.call(
                [
                    "foamDictionary",
                    "%s/%s/%s" % (self.path_, self.startTime_, v[1]),
                    "-entry",
                    "boundaryField.%s" % v[2],
                    "-set",
                    """{
                                type            externalCoupledNew;
                                commsDir        "%s";
                                waitInterval    0;
                                //calcFrequency   1;
                                calcInterval    %s;
                                file            data_OpenFOAM_%s_%s;
                                initByExternal  0;
                            }"""
                    % (
                        self.comDir_,
                        self.timeStep_,
                        self.name_,
                        v[1],
                    ),
                ],
                stdout=subprocess.DEVNULL,
            )
            subprocess.call(
                ["createExternalCoupledPatchGeometryNew", "-case", self.path_, v[1]],
                stdout=subprocess.DEVNULL,
            )
            os.system("foamListTimes -rm -case %s" % self.path_)
