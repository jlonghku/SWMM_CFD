import os, threading
from importlib import import_module
import tools as tl


class timeControl(object):
    # timeControl module
    @classmethod
    def clsInit(cls):
        # current time for cases
        cls.times_ = []
        # current timestep for cases
        cls.timeSteps_ = []
        # end time for cases
        cls.endTimes_ = []

    def __init__(self, dict):

        # start time
        self.startTime_ = dict.get("startTime")
        # end time
        self.endTime_ = dict.get("endTime")
        # time step
        self.timeStep_ = dict.get("timeStep", dict.get("deltaT"))
        # current time
        self.time_ = self.startTime_
        # sequence of timeControl
        self.num_ = len(timeControl.times_)
        # current time for cases
        timeControl.times_.append(self.time_)
        timeControl.endTimes_.append(self.endTime_)
        timeControl.timeSteps_.append(self.timeStep_)

    def time(self):
        # return Time
        return self.time_

    def clsNext(self):
        # next runTime for all cases
        nextT = [
            i + j if i + j <= self.endTime_ and i > 0 else self.clsEnd()
            for i, j in zip(timeControl.timeSteps_, timeControl.times_)
        ]
        return nextT.index(min(nextT)) if min(nextT) < self.clsEnd() else self.num_

    def set(self, time):
        # set time for current case
        if time >= self.endTime_:
            self.setTimeStep(0)
        timeControl.times_[self.num_] = self.time_ = time

    def setTimeStep(self, timeStep):
        # set timestep for current case
        timeControl.timeSteps_[self.num_] = self.timeStep_ = timeStep

    def clsEnd(self):
        # end Time for all cases
        return max(timeControl.endTimes_)

    def isNext(self):
        # check if the current case should run
        return self.time_ < self.endTime_ and self.num_ == self.clsNext()

    def notStop(self):
        return any(timeControl.timeSteps_)


class boundaryControl(object):
    # boundaryControl module
    @classmethod
    def clsInit(cls):
        # boundaries for cases
        cls.boundaries_ = {}

    def __init__(self, boundary):
        # inital boundary condition for case
        self.boundary_ = boundary
        for v in boundary:
            boundaryControl.boundaries_[v[0]] = v[3]

    def set(self, boundary):
        # set boundary for current case
        self.boundary_ = boundary
        for v in boundary:
            boundaryControl.boundaries_[v[0]].update(v[3])

    def boundary(self):
        # return boundary of current case
        for v in self.boundary_:
            v[3].update(boundaryControl.boundaries_[v[0]])
        return self.boundary_


class runControl(object):
    # runControl module
    jobs_ = 0
    sem_ = []

    @classmethod
    def clsInit(cls, job):
        # add runtime and semaphore for each sub case, total number of cases n, set the first sem to 1
        # semaphore list, set sem for each running model
        cls.sem_ = []
        cls.sem_.append(threading.Semaphore())
        for i in range(job - 1):
            cls.sem_.append(threading.Semaphore(0))
        # count the cases num

    def __init__(self):
        # set the wait/notify sem for threading
        self.wait_ = runControl.jobs_
        if runControl.jobs_ < len(runControl.sem_) - 1:
            self.notify_ = self.wait_ + 1
        else:
            self.notify_ = 0
        # add the current jobs num
        runControl.jobs_ += 1

    def acquire(self, wait):
        runControl.sem_[wait].acquire()

    def release(self, notify):
        runControl.sem_[notify].release()


# runModel module


class runModel(threading.Thread):

    # import external module of models to dict cls.models
    @classmethod
    def clsImportModels(cls, models):
        cls.models_ = {}
        for i in models:
            cls.models_[i] = import_module(i)

    @classmethod
    def clsInit(cls, inp):
        # inital the parameters
        # set case path and com path
        cls.dir_ = inp.dir
        # enable edit of folders
        os.system("sudo chmod 777 -R " + cls.dir_)
        cls.comDir_ = cls.dir_ + "/comms"
        tl.cleanDir(cls.comDir_)

        # inital class timeControl, boundaryControl and runControl
        timeControl.clsInit()
        boundaryControl.clsInit()
        runControl.clsInit(len(inp.cases))

        # add each case
        cls.cases_ = []
        for i in inp.cases:
            i["path"] = cls.dir_ + "/" + i["model"] + "/" + i["name"]
            i["comDir"] = cls.comDir_
            cls.cases_.append(cls(i))

    @classmethod
    def clsRun(cls):
        # run the class
        for case in cls.cases_:
            case.setDaemon(True)
            case.start()

        # check if completed
        while True:
            alive = False
            for work in cls.cases_:
                alive = alive or work.isAlive()
            if not alive:
                print("End of All Cases!")
                break

    def __init__(self, inp):
        # init one case
        # start threading
        threading.Thread.__init__(self)
        self.case_ = runModel.models_[inp["model"]].case(inp)
        # update timeControl
        self.tc = timeControl(inp["timeControl"])
        # update boundaryControl
        self.bc = boundaryControl(inp["boundaryControl"])
        # update runControl
        self.rc = runControl()

    def run(self):
        # first running
        # setup Semaphore for subCases
        self.con_child = threading.Semaphore(0)
        self.con_father = threading.Semaphore(0)
        self.case_.getSem(self.con_father, self.con_child)
        self.case_.start()

        # run the next time step
        while self.tc.time_ < self.tc.endTime_:
            self.rc.acquire(self.rc.wait_)
            while self.tc.isNext():
                self.case_.setBoundary(self.bc.boundary())
                self.con_child.release()
                self.con_father.acquire()
                self.tc.set(self.case_.time())
                self.bc.set(self.case_.boundary())
            self.rc.release(self.rc.notify_)
        print(
            "End of case: %s-%s" % (self.case_.dict["model"], self.case_.dict["name"])
        )
        while self.tc.notStop():
            self.rc.acquire(self.rc.wait_)
            self.rc.release(self.rc.notify_)
