import os, shutil, ast
import ast, re
import numpy as np


def turn(s, char1, char2):
    if not isinstance(s, str):
        s = str(s)
    return re.sub(r"\(.*?\)", lambda x: char2.join(x.group().split(char1)), s)


def resetOpenFOAM(path):
    for f in os.listdir(path):
        if not os.path.isdir(f):
            fi = os.path.join(path, f)
            if not fi.endswith(".orig"):
                bakfile(fi)
            else:
                shutil.copyfile(fi, os.path.splitext(fi)[0])


def bakfile(f1):
    if os.path.isfile(f1):
        if not os.path.exists(f1 + ".orig"):
            shutil.copyfile(f1, f1 + ".orig")
        else:
            shutil.copyfile(f1 + ".orig", f1)


def readBoundary_OpenFOAM(path):
    # read boundary output file from OpenFOAM
    if os.path.exists(path):
        with open(path) as f:
            s = f.read()
            s1 = turn(s, " ", ",")
            return ast.literal_eval(s1)


def writeBoundary_OpenFOAM(data, k, path):
    # write boundary output file for OpenFOAM
    if data:
        with open(path, "w") as f:
            for v in data:
                if k == v[1]:
                    f.writelines([v[2], "\n"])
                    f.writelines([v[1], "\n"])
                    for j in range(len(v[3]["value_OpenFOAM"])):
                        f.write(turn(v[3]["value_OpenFOAM"][j], ",", ""))
                        f.write(" ")
                        f.write(turn(v[3]["snGrad_OpenFOAM"][j], ",", ""))
                        f.write(" ")
                        f.write(turn(v[3]["magSf_OpenFOAM"][j], ",", ""))
                        f.write("\n")
                    if isinstance(v[3]["snGrad_OpenFOAM"][0], tuple):
                        return "v"
                    else:
                        return "s"


def cleanDir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)
    os.system("sudo chmod 777 -R " + path)


def readTime_OpenFOAM(files, lockFile):
    while True:
        if not os.path.exists(lockFile):
            if not os.path.exists(files):
                time = [0, 0]
            else:
                with open(files, "r") as f:
                    lines = f.readlines()
                    time = lines[0].split()
            return float(time[0]), float(time[1])


def setTime_OpenFOAM(path, dict):
    # setup the time control file
    os.system(
        "foamDictionary %s/system/controlDict -entry %s  -set %g >/dev/null"
        % (path, "startTime", dict["startTime"])
    )
    os.system(
        "foamDictionary %s/system/controlDict -entry %s  -set %g >/dev/null"
        % (path, "endTime", dict["endTime"])
    )
    os.system(
        "foamDictionary %s/system/controlDict -entry %s  -set %g >/dev/null"
        % (path, "writeInterval", dict["timeStep"])
    )


def readNCorr_OpenFOAM(path):
    return int(
        os.popen(
            "foamDictionary %s/system/fvSolution -entry PIMPLE.nCorrectors -value"
            % path
        ).read()
    )


def transferBoundary(boundary):
    # format the boundary value
    for v in boundary:
        if len(v[3]) > 1:
            if v[3].get("model", 0) == "SWMM":
                if v[3].get("value_OpenFOAM", False):
                    magSfs = v[3]["magSf_OpenFOAM"]
                    values = v[3]["value_OpenFOAM"]
                    snGrads = v[3]["snGrad_OpenFOAM"]
                    Sfs = v[3]["Sf_OpenFOAM"]
                    val1 = 0
                    if isinstance(values[0], tuple):
                        v[3]["phi"] = 0
                        for j in range(len(values)):
                            val1 += np.dot(np.array([1, 1, 1]), np.array(Sfs[j]))
                            v[3]["phi"] += np.dot(np.array(values[j]), np.array(Sfs[j]))
                        if v[3]["phi"] != 0:
                            v[3]["value_OpenFOAM"] = [
                                tuple(np.array(i) * v[3]["value_SWMM"] / v[3]["phi"])
                                for i in values
                            ]
                        else:
                            v[3]["value_OpenFOAM"] = [
                                tuple(np.array([1, 1, 1]) * v[3]["value_SWMM"] / val1)
                                for i in values
                            ]
                    else:
                        v[3]["avg"] = 0
                        for j in range(len(values)):
                            v[3]["avg"] += (
                                magSfs[j] * values[j] / sum(magSfs)
                                if sum(magSfs) != 0
                                else 0
                            )
                        if v[3]["avg"] != 0:
                            v[3]["value_OpenFOAM"] = [
                                i * v[3]["value_SWMM"] / v[3]["avg"] for i in values
                            ]
            elif v[3].get("model", 0) == "OpenFOAM":
                magSfs = v[3]["magSf_OpenFOAM"]
                values = v[3]["value_OpenFOAM"]
                snGrads = v[3]["snGrad_OpenFOAM"]
                Sfs = v[3]["Sf_OpenFOAM"]
                if isinstance(values[0], tuple):
                    v[3]["phi"] = 0
                    for j in range(len(values)):
                        v[3]["phi"] += np.dot(np.array(values[j]), np.array(Sfs[j]))
                    v[3]["value_SWMM"] = v[3]["phi"]
                else:
                    v[3]["avg"] = 0
                    for j in range(len(values)):
                        v[3]["avg"] += magSfs[j] * values[j] / sum(magSfs) / 9810
                    v[3]["value_SWMM"] = v[3]["avg"]
            
    return boundary


###########################################
