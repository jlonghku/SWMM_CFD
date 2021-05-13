import os,shutil


def islock(path):
    for f in os.listdir(path):
        if f.endswith('.lock'):
            return True
    return False

def cleandir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)

def listdirs(path):
    dirs = []
    names = []
    for f in os.listdir(path):
        d = os.path.join(path, f)
        if os.path.isdir(d):
            dirs.append(d)
            names.append(f)
    dirs.sort()
    names.sort()
    return list(zip(dirs, names))


def checkState(dirs):
    import os
    if not os.path.exists(dirs):
        os.mkdir(dirs)
    islock = False
    files = os.listdir(dirs)
    for i in files:
        islock = True if i == 'OpenFOAM.lock' else islock
    return islock


def isRun(dirs, init, sw_time, of_time):
    islock = checkState(dirs)
    if (islock == False) & (init == 1) & (sw_time <= of_time):
        return 1
    elif (islock == False) & (init == 1) & (sw_time > of_time):
        return 2
    elif (islock == False) & (init == 0) & (sw_time < of_time):
        return 1
    elif (islock == False) & (init == 0) & (sw_time >= of_time):
        return 2
    else:
        return 3


def readTime(files):
    if not os.path.exists(files):
        time=0
    else:
        with open(files, 'r') as f:
            lines = f.readlines()
            if len(lines) <= 2:
                time = 0
            else:
                time = float(lines[-1].split()[0])
    return time


import numpy as np
import re


def read_data(dataname):
    with open(dataname) as f:
        next(f)
        p1 = 0.0
        flux = 0.0
        for line in f:
            tp = re.compile(r'[(](.*?)[)]')
            p = re.split(tp, line)
            p0 = list(
                filter(lambda s: s and (type(s) != str or len(s.strip()) > 0),
                       p))
            p1 = float(p0[0])
            p2 = np.fromstring(p0[1], dtype='float', sep=' ')
            p3 = np.fromstring(p0[2], dtype='float', sep=' ')
            flux += p1 * np.dot(p2, p3)
        print(flux)
    return flux


def outswmm(comdir, node_object, patchlist):
    with open(comdir + "/swmm.out", "w") as f:
        for patchi in patchlist:
            f.writelines([
                patchi[1],
                " ",
                str(node_object[patchi[0]].total_outflow),
                "\n",
            ])
