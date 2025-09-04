import threading
from importlib import import_module
import tools as tl
from dateutil.parser import parse
from datetime import timedelta


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
        # start for cases
        cls.starts_ = []

    def __init__(self, dt):
        # parse str/num to datetime (s)
        dict = {}
        for k, v in dt.items():
            dict[k] = parse(v) if isinstance(v, str) else timedelta(0, v)
        # offSet
        self.offSet_ = dict["offSet"]
        # start time
        self.startTime_ = dict["startTime"] + self.offSet_
        # end time
        self.endTime_ = dict["endTime"] + self.offSet_
        # time step
        self.timeStep_ = dict["timeStep"]
        # set time
        self.time_ = self.startTime_
        # sequence of timeControl
        self.num_ = len(timeControl.times_)
        # add into class for all cases
        timeControl.endTimes_.append(self.endTime_)
        timeControl.timeSteps_.append(self.timeStep_)
        timeControl.times_.append(self.time_)

        self.start_ = False
        timeControl.starts_.append(False)

    def set(self, time):
        # set time for current case
        if time >= self.endTime_:
            self.setTimeStep(timedelta(0))
        timeControl.times_[self.num_] = self.time_ = time

    def setStart(self):
        # start case
        timeControl.starts_[self.num_] = self.start_ = True

    def setTimeStep(self, timeStep):
        # set timestep for current case
        timeControl.timeSteps_[self.num_] = self.timeStep_ = timeStep

    def isRun(self):
        # check if the current case is running
        return (
            self.time_ < self.endTime_ and self.time_ + self.timeStep_ <= self.endTime_
        )

    def isNext(self):
        # check if the current case should run now
        nextT = [
            i + j if i + j <= self.endTime_ and i > timedelta(0) else self.endTime_
            for i, j in zip(timeControl.timeSteps_, timeControl.times_)
        ]
        return nextT[self.num_] == min(nextT)

    def notStop(self):
        # check if all cases still run
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
        # update and return boundary of current case
        for v in self.boundary_:
            v[3].update(boundaryControl.boundaries_[v[0]])
        return self.boundary_

    def printPhi(self):
        for v in self.boundary_:
            print("Phi of %s: %s" % (v[0], v[3].get("phi", "No Value!")))


class runControl(object):
    # runControl module

    @classmethod
    def clsInit(cls, job):
        # add runtime and semaphore for each sub case, total number of cases n, set the first sem to 1
        # semaphore list, set sem for each running model
        cls.num_ = 0
        cls.sem_ = []
        cls.sem_.append(threading.Semaphore())
        for i in range(job - 1):
            cls.sem_.append(threading.Semaphore(0))

    def __init__(self):
        # set the wait/notify sem for threading
        self.wait_ = runControl.num_
        if runControl.num_ < len(runControl.sem_) - 1:
            self.notify_ = self.wait_ + 1
        else:
            self.notify_ = 0
        # add the current jobs num
        runControl.num_ += 1

    def acquire(self):
        # wait for other cases
        runControl.sem_[self.wait_].acquire()

    def release(self):
        # notify other cases of running
        runControl.sem_[self.notify_].release()

    def start(self):
        # start current case
        runControl.sem_[self.wait_].release()


class runModel(threading.Thread):
    # runModel module

    @classmethod
    def clsImportModels(cls, models):
        # import external module of models to dict cls.models
        cls.models_ = {}
        for i in models:
            cls.models_[i] = import_module(i)

    @classmethod
    def clsInit(cls, inp):
        # inital the parameters
        # set case path and com path
        cls.dir_ = inp.dir
        cls.comDir_ = cls.dir_ + "/comms"
        tl.cleanDir(cls.comDir_)

        # inital class timeControl, boundaryControl and runControl
        timeControl.clsInit()
        boundaryControl.clsInit()
        runControl.clsInit(len(inp.cases))

        # add case
        cls.cases_ = []
        for i in inp.cases:
            i["path"] = "%s/%s/%s" % (cls.dir_, i["model"], i["name"])
            i["comDir"] = cls.comDir_
            cls.cases_.append(cls(i))

    @classmethod
    def clsRun(cls):
        # run all cases
        for case in cls.cases_:
            case.setDaemon(True)
            case.start()

        # check if all cases are completed
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
        # update timeControl
        self.tc = inp["tc"] = timeControl(inp["timeControl"])
        # update boundaryControl
        self.bc = inp["bc"] = boundaryControl(inp["boundaryControl"])
        # update runControl
        self.rc = inp["rc"] = runControl()
        # initalize the case using customed OpenFOAM/SWMM.py class
        self.case_ = runModel.models_[inp["model"]].case(inp)

    def run(self):
        # setup Semaphore for cases
        self.con_child = threading.Semaphore(0)
        self.con_father = threading.Semaphore(0)
        self.case_.getSem(self.con_father, self.con_child)

        # before running the case
        while True:
            self.rc.acquire()
            if self.tc.isNext:
                self.rc.start()
                break
            else:
                self.rc.release()

        # start to run the case
        self.tc.setStart()
        self.case_.start()

        # loop for all time step
        while not self.case_.end():
            self.rc.acquire()
            if self.tc.isNext():
                self.case_.setBOUNDARY(self.bc.boundary())
                self.con_child.release()
                self.con_father.acquire()
                self.tc.set(self.case_.TIME())
                self.bc.set(self.case_.BOUNDARY())

                print(
                    "%s-%s Time (Recorded/Running): \n%s (%s)"
                    % (
                        self.case_.dict["model"],
                        self.case_.dict["name"],
                        self.case_.TIME(),
                        self.case_.time_,
                    )
                )
                # self.bc.printPhi()
            self.rc.release()

        print(
            "End of case: %s-%s" % (self.case_.dict["model"], self.case_.dict["name"])
        )
        # wait for other cases to finish
        while self.tc.notStop():
            self.rc.acquire()
            self.rc.release()
