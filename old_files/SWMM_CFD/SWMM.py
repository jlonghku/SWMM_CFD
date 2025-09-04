from pyswmm import Simulation, Nodes
import threading
import numpy as np
import tools as tl


class case(threading.Thread):
    def __init__(self, inp):
        # construct a new case (essential function)
        threading.Thread.__init__(self)
        self.dict = inp

        # setup parameters for pyswmm
        self.offSet_ = inp["tc"].offSet_
        self.startTime_ = inp["tc"].startTime_ - self.offSet_
        self.time_ = self.startTime_
        self.endTime_ = inp["tc"].endTime_ - self.offSet_
        self.timeStep_ = inp["tc"].timeStep_

        # setup boundary for pyswmm
        self.boundary_ = inp["bc"].boundary()

        # setup simulation for pyswmm
        self.sim = Simulation(self.dict["path"])
        self.node = Nodes(self.sim)
        self.sim.start_time = self.startTime_
        self.sim.end_time = self.endTime_ + self.timeStep_
        self.sim.step_advance(inp["timeControl"]["timeStep"])

    def run(self):
        # loop for SWMM simulation (essential function)
        print(
            "SWMM-%s time:\n%s " % (self.dict["name"], self.startTime_ + self.offSet_)
        )
        self.con_child.acquire()
        for step in self.sim:
            # print("(internal) SWMM-%s time:\n%s " % (self.dict["name"],self.sim.current_time))
            self.update()
            self.con_father.release()
            if self.sim.current_time < self.endTime_:
                self.con_child.acquire()

    def getSem(self, father, child):
        # setup Semaphore for father and child threads to sync data (essential function)
        self.con_child = child
        self.con_father = father

    def TIME(self):
        # return time with offSet to father thread (essential function)
        return self.time_ + self.offSet_

  

    def end(self):
        # check if the case is finished
        return self.time() + self.offSet_ >= self.endTime_

    def BOUNDARY(self):
        # return boundary data to father thread (essential function)
        return self.boundary_

    def setBOUNDARY(self, boundary):
        # get boundary conditions from father thread (essential function)
        self.boundary_ = tl.transferBoundary(boundary)
        for v in self.boundary_:
            if len(v[3]) > 1 and "model" in v[3].keys():
                if self.node[v[2]].is_outfall():
                    self.node[v[2]].outfall_stage(v[3]["value_SWMM"])
                else:
                    self.node[v[2]].generated_inflow(v[3]["value_SWMM"])

    ######################################################################
    # additional functions
    def update(self):
        # update all data
        self.updateTime()
        self.updateBoundary()

    def time(self):
        # return internal time for current case
        return self.time_

    def updateTime(self):
        # update time
        self.time_ = self.sim.current_time

    def updateBoundary(self):
        for v in self.boundary_:
            v[3]["model"] = "SWMM"
            if v[1] == "U":
                v[3]["value_SWMM"] = self.node[v[2]].total_inflow
            elif v[1] == "p":
                v[3]["value_SWMM"] = self.node[v[2]].depth
