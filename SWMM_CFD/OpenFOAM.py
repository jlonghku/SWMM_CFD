import os
import subprocess
import tools as tl
import threading
import numpy as np
from datetime import timedelta


class case(threading.Thread):
    def __init__(self, inp):
        # construct a new case (essential function)
        threading.Thread.__init__(self)
        # data to create a case, include parameters:
        self.dict = inp

        # pre-processing
        ## setup path and filenames
        self.name_ = inp["name"]
        self.path_ = inp["path"]
        self.comDir_ = inp["comDir"]
        self.lockFile_ = self.comDir_ + "/OpenFOAM_" + self.name_ + ".lock"

        ## setup time (relative)
        self.offSet_ = inp["tc"].offSet_
        self.startTime_ = inp["timeControl"]["startTime"]
        self.time_ = self.startTime_
        self.endTime_ = inp["timeControl"]["endTime"]
        self.timeStep_ = inp["timeControl"]["timeStep"]
        tl.setTime_OpenFOAM(self.path_, inp["timeControl"])

        ## clean time record
        self.timeFile_ = "%s/time.log" % self.path_
        if os.path.exists(self.timeFile_):
            os.remove(self.timeFile_)

        ## setup boundary
        self.boundary_ = inp["bc"].boundary()
        self.modifyBoundary()
        self.outFile_ = {
            k: "%s/data_OpenFOAM_%s_%s.out" % (self.comDir_, self.name_, k)
            for k in set([v[1] for v in self.boundary_])
        }
        nCorrectors_ = tl.readNCorr_OpenFOAM(self.path_)
        self.Correctors_ = [
            nCorrectors_,
            nCorrectors_,
            timedelta(0, self.time_) + self.offSet_,
        ]

    def run(self):
        # loop for OpenFOAM simulation (essential function)
        ## first run
        # print("(internal) OpenFOAM-%s time:\n %s" % (self.name_,self.startTime_))
        first = True
        print(
            "OpenFOAM-%s time:\n%s"
            % (self.name_, timedelta(0, self.startTime_) + self.offSet_)
        )
        ## run
        while not self.end():
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
                self.conRun()
                if self.Correctors_[0] == 1:
                    self.Correctors_[0] = self.Correctors_[1]
                    self.Correctors_[2] = timedelta(0, self.time_) + self.offSet_
                else:
                    self.Correctors_[0] -= 1
            self.wait()
            self.update()
            # print("(internal) OpenFOAM-%s time:\n %s" % (self.name_,self.time()))
            self.con_father.release()

    def getSem(self, father, child):
        # setup Semaphore for father and child threads to sync data (essential function)
        self.con_child = child
        self.con_father = father

    def TIME(self):
        # return time with offSet to father thread (essential function)
        return self.Correctors_[2]

    def end(self):
        # check if the case is finished (essential function)
        return tl.readTime_OpenFOAM(self.timeFile_, self.lockFile_)[0] >= self.endTime_

    def BOUNDARY(self):
        # return boundary conditions to father thread (essential function)
        return self.boundary_

    def setBOUNDARY(self, boundary):
        # get boundary conditions from father thread (essential function)
        self.boundary_ = tl.transferBoundary(boundary)
        for k, v in self.outFile_.items():
            if os.path.exists(v):
                fieldType = tl.writeBoundary_OpenFOAM(self.boundary_, k, v)

                bcFiles = (
                    "%s patchPoints_OpenFOAM_%s_%s patchFaces_OpenFOAM_%s_%s data_OpenFOAM_%s_%s"
                    % (self.comDir_, self.name_, k, self.name_, k, self.name_, k)
                )

                mapcmd = "mapPatch -%s -toFiles \( %s.in \) -fromFiles \( %s.out \)" % (
                    fieldType,
                    bcFiles,
                    bcFiles,
                )

                subprocess.call(mapcmd, shell=True, stdout=subprocess.DEVNULL)
                # os.system(mapcmd)

    ######################################################################
    # additional functions
    def conRun(self):
        # resume OpenFOAM solver
        os.system("touch " + self.lockFile_)

    def isWait(self):
        # check the running state of OpenFOAM solver
        isOut = False
        for v in self.outFile_.values():
            isOut = isOut or os.path.exists(v)
        isStop = (
            tl.readTime_OpenFOAM(self.timeFile_, self.lockFile_)[0] == self.endTime_
        )
        return os.path.exists(self.lockFile_) or not (isStop or isOut)

    def wait(self):
        # wait for solver stopping
        while self.isWait():
            pass

    def time(self):
        # return internal time for current case
        return self.time_

    def update(self):
        # update time and boundary data
        self.updateTime()
        self.updateBoundary()

    def updateTime(self):
        # update time
        self.time_ = round(sum(tl.readTime_OpenFOAM(self.timeFile_, self.lockFile_)))

    def updateBoundary(self):
        # update boundary
        for v in self.outFile_.values():
            if os.path.exists(v):
                b = tl.readBoundary_OpenFOAM(v)
                for v1 in b:
                    for v2 in self.boundary_:
                        if v1[0] == v2[1] and v1[1] == v2[2]:
                            v2[3].update(v1[2])

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

        self.nCorrectors_ = 2
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
            os.system(
                "foamListTimes -rm -case %s -time %s:"
                % (self.path_, self.startTime_ + self.timeStep_)
            )
