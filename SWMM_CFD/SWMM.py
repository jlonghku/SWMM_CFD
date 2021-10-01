from pyswmm import Simulation, Nodes
from multiprocessing import Pool
import threading, tools as tl
from datetime import timedelta
import numpy as np


class case(threading.Thread):
    def __init__(self, inp):
        # construct a new case (essential function)
        threading.Thread.__init__(self)
        self.dict = inp
        # setup parameters for pyswmm
        self.startTime_ = self.dict["timeControl"]["startTime"]
        self.time_ = self.startTime_
        self.timeStep_ = self.dict["timeControl"]["timeStep"]
        self.endTime_ = self.dict["timeControl"]["endTime"]
        self.boundary_ = self.dict["boundaryControl"]
        self.path_ = self.dict["path"]

        # setup simulation for pyswmm
        self.sim = Simulation(self.path_)
        self.node = Nodes(self.sim)

        self.sim.start_time = self.sim.start_time + timedelta(0, self.startTime_, 0)
        self.sim.end_time = self.sim.start_time + timedelta(
            0, self.endTime_ - self.startTime_ + self.timeStep_
        )
        # self.sim.step_advance(self.timeStep_)

    def run(self):
        # loop for SWMM simulation (essential function)
        # print("\nSWMM-%s time: " % self.dict["name"])
        # print(self.sim.start_time)
        for step in self.sim:
            self.con_child.acquire()
            print("SWMM-%s time: " % self.dict["name"])
            print(self.sim.current_time)
            self.update()
            self.con_father.release()

    def getSem(self, father, child):
        # setup Semaphore for father and child threads to sync data (essential function)
        self.con_child = child
        self.con_father = father

    def boundary(self):
        # return boundary data (essential function)
        return self.boundary_

    def time(self):
        # return time (essential function)
        return self.time_

    def update(self):
        # update all data
        self.updateTime()
        self.updateBoundary()

    def updateTime(self):
        self.time_ = (
            self.startTime_
            + (self.sim.current_time - self.sim.start_time).total_seconds()
        )

    def updateBoundary(self):
        for v in self.boundary_:
            v[3]["model"] = "SWMM"
            if v[1] == "U":
                v[3]["value_SWMM"] = self.node[v[2]].total_inflow
            elif v[1] == "p":
                v[3]["value_SWMM"] = self.node[v[2]].depth

    def setBoundary(self, boundary):
        # get boundary conditions from father thread (essential function)
        self.boundary_ = boundary
        self.transferBoundary()
        self.loadBoundary()

    def transferBoundary(self):
        # format boundary conditions from other model (e.g., OpenFOAM, etc.)
        for v in self.boundary_:
            if "model" in v[3].keys():
                if v[3].get("model", 0) == "OpenFOAM":
                    magSfs = v[3]["magSf_OpenFOAM"]
                    values = v[3]["value_OpenFOAM"]
                    snGrads = v[3]["snGrad_OpenFOAM"]
                    Sfs = v[3]["Sf_OpenFOAM"]
                    val = 0
                    if isinstance(values[0],tuple):
                        for j in range(len(values)):
                            val += np.dot(values[j], Sfs[j])
                        v[3]["value_SWMM"] = val
                    else:
                        for j in range(len(values)):
                            val += magSfs[j] * values[j]
                        v[3]["value_SWMM"] = val / sum(magSfs)/9810

    def loadBoundary(self):
        for v in self.boundary_:
            if "model" in v[3].keys():  
                if self.node[v[2]].is_outfall():
                    self.node[v[2]].outfall_stage(v[3]["value_SWMM"])
                else:
                    self.node[v[2]].generated_inflow(v[3]["value_SWMM"])
