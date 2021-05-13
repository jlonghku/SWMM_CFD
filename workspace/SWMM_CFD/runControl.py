import threading
import tools as tl


class timeControl(object):
    def __init__(self, dict):
        # start time
        timeControl.startTime = dict.get('startTime')
        # end time
        timeControl.endTime = dict.get('endTime')
        # time step
        timeControl.timeStep = dict.get('timeStep')

    def update(self, dict):
        # start time
        self.startTime = dict.get('startTime', self.startTime)
        # end time
        self.endTime = dict.get('endTime', self.endTime)
        # time step
        self.timeStep = dict.get('timeStep', self.timeStep)


class modelControl(object):
    # initalize the model with parameters
    @classmethod
    def clsInit(cls, clsPara):
        # set path
        modelControl.caseDir = clsPara.caseDir
        modelControl.comDir = modelControl.caseDir + '/comms'
        tl.cleandir(modelControl.comDir)

        #set boundary
        modelControl.patchlist = clsPara.patchlist

    def __init__(self, para):
        pass

    def case(self, para):
        pass


class runControl(object):
    # add runtime and semaphore for each model, total number of models n, set the first sem to 1
    @classmethod
    def clsInit(cls, models):
        # semaphore list, set sem for each running model
        runControl.sem = []
        runControl.sem.append(threading.Semaphore())
        for i in range(len(models) - 1):
            runControl.sem.append(threading.Semaphore(0))
        # models to be launched
        runControl.models = []
        for i in models:
            runControl.models.append(i)
