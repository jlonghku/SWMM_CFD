from pyswmm import Simulation, Nodes
import os
import tools as tl


class Case(object):
    def __init__(self, inp):
        self.dict = inp

    def get(self, info):
        return self.dict.get(info)

    def run(self, dir, tc, rc):
        self.load(dir)
    # start loop
        for step in self.sim:
            print(self.time())
            # get lock
            rc.acquire(rc.wait)
            # running until reaching next time step
            if (self.time() + tc.timeStep == tc.nextmin()):

                # update boundary
                self.updateBoundary()
                # update time
                tc.setTime(rc.wait, self.time())
                # switch to next step
                rc.release(rc.wait)

            # run next subCase
            else:
                # output results
                self.output()
                # switch to next model
                rc.release(rc.notify)

        # skip running of current model
        while self.time() >= tc.endTime:
            if (tc.timestep != 0):
                tc.setTime(0)
                tc.setTimeStep(0)
            rc.acquire(rc.wait)
            rc.release(rc.notify)
        self.sim.close()

    def load(self, dir):
        self.path = dir + '/' + self.dict.get(
            'model') + '/' + self.dict.get('name')
        self.sim = Simulation(self.path)

    def time(self):
        return (self.sim.current_time-self.sim.start_time).total_seconds()

    def updateBoundary(self):
        pass
        #os.system("mapPatch -files")

    def output(self):
        pass
        # tl.outswmm(self.comdir, Nodes(self.sim), self.patchlist)
