import threading,os
from importlib import import_module
import tools as tl


# timeControl module
class timeControl(object):
    @classmethod
    def clsInit(cls):
        # current time for cases
        timeControl.times = []
        # current timestep for cases
        timeControl.timeSteps = []
        # end time for cases
        timeControl.endTimes = []

    def __init__(self, dict):

        # start time
        self.startTime = dict.get('startTime', 0)
        # end time
        self.endTime = dict.get('endTime', 1)
        # time step
        self.timeStep = dict.get('timeStep', dict.get('deltaT',0.1))
        # current time
        self.time = self.startTime
        # num of timeControl
        self.num = len(timeControl.times)
        # current time for cases
        timeControl.times.append(self.time)
        timeControl.timeSteps.append(self.timeStep)
        timeControl.endTimes.append(self.endTime)

    def getTime(self):
        return self.time

    def nextMin(self):
        next = timeControl.timeSteps + timeControl.times
        return min(next[next > 0])

    def setTime(self,  time):
        self.time = time
        timeControl.times[self.num] = time

    def next(self):
        self.setTime(self.time+self.timeStep)

    def setTimeStep(self,  timeStep):
        self.timeStep = timeStep
        timeControl.timeSteps[self.num] = timeStep

    def end(self):
        return max(timeControl.endTimes)

# boundaryControl module


class boundaryControl(object):
    pass


# runControl module
class runControl(object):
    jobs = 0
    sem = []

    @classmethod
    def clsInit(cls, jobs):
        # add runtime and semaphore for each sub case, total number of cases n, set the first sem to 1
        # semaphore list, set sem for each running model
        runControl.sem = []
        runControl.sem.append(threading.Semaphore())
        for i in range(jobs - 1):
            runControl.sem.append(threading.Semaphore(0))
        # count the cases num

    def __init__(self):
        # set the wait/notify sem for threading
        self.wait = runControl.jobs
        if runControl.jobs < len(runControl.sem) - 1:
            self.notify = self.wait + 1
        else:
            self.notify = 0
        # add the current jobs num
        runControl.jobs += 1

    def acquire(self, wait):
        runControl.sem[wait].acquire()

    def release(self, notify):
        runControl.sem[notify].release()

# runModel module


class runModel(threading.Thread):
    tc = 0
    rc = 0
    bc = 0

    # import external module of models to dict cls.models
    @classmethod
    def clsImportModels(cls, models):
        cls.models = {}
        for i in models:
            cls.models[i] = import_module(i)

    # inital the parameters
    @classmethod
    def clsInit(cls, inp):
        # set case path and com path
        cls.dir = inp. dir
        # enable edit of folders
        os.system('sudo chmod 777 -R ' + cls.dir)
        cls.comDir = cls.dir + '/comms'
        #tl.cleandir(cls.comDir)

        # inital class timeControl and runControl
        timeControl.clsInit()
        runControl.clsInit(len(inp.cases))

        # add each case
        cls.cases = []

        for i in inp.cases:
            i['path'] = cls.dir+'/'+i['model']+'/'+i['name']
            i['comDir'] = cls.comDir
            cls.cases.append(cls(i))

    # run the class
    @classmethod
    def clsRun(cls):
        for case in cls.cases:
            case.setDaemon(True)
            case.start()

        # check if completed
        while True:
            alive = False
            for work in cls.cases:
                alive = alive or work.isAlive()
                if not alive:
                    break

    # init the control of a model
    def __init__(self, inp):
        # start threading
        threading.Thread.__init__(self)
        self.case = runModel.models[inp.get('model')].case(inp)
        # update timeControl
        self.tc = timeControl(inp.get('timeControl'))
        # update runControl
        self.rc = runControl()

    def run(self):
        # first running
        self.case.start()
        while self.tc.time < self.tc.endTime:
            self.rc.acquire(self.rc.wait)
            while self.case.time()<=self.tc.time:
                self.case.updateBoundary()
                self.case.continueRun()
                while self.case.isRun():
                    pass           
            # self.case.updateBoundary()
            self.tc.next()
            self.rc.release(self.rc.notify)
        print('End of '+self.case.get('path'))
        while self.tc.time < self.tc.end():
            self.rc.acquire(self.rc.wait)
            self.rc.release(self.rc.notify)
        print('End of All')
        
