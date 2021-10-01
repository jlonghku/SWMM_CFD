import os, shutil, json, ast
import ast, re


def dicMeg(dic1, dic2):
    # merge dict2 to dict1
    for i in dic2:
        if i in dic1:
            if type(dic1[i]) is dict and type(dic2[i]) is dict:
                dicMeg(dic1[i], dic2[i])
        else:
            dic1[i] = dic2[i]


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


def readDict(path):
    path = "/home/jlong/workspace/SWMM_CFD/Case/comms/data_OpenFOAM_cavity.out"
    with open(path) as f:
        f1 = f.read().replace(" ", ",")
        data = ast.literal_eval(f1)
        print(data["movingWall"]["value"][0])
        return ast.literal_eval(f1)


def save(dict, path):
    with open(path, "w") as outfile:
        json.dump(dict, outfile, ensure_ascii=False)
        outfile.write("\n")


def load(path):
    with open(path, "r") as loadfile:
        new_dict = json.load(loadfile)
        return new_dict


def cleanDir(path):
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


def readTime_OpenFOAM(files):
    
    if not os.path.exists(files):
        time = [0,0]
    else:
        with open(files, "r") as f:
            lines = f.readlines()
            time = lines[-1].split()
    return float(time[0])+float(time[1])


###########################################
