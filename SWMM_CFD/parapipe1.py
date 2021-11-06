import os

# Dir
dir = os.path.dirname(os.path.realpath(__file__)) + "/Case"

# timeControl dict
timeControl = {"startTime": 30, "endTime": 600, "timeStep": 30,"offSet":"11/01/2017"}
timeControl1 = {"startTime": "11/01/2017", "endTime": "11/01/2017 00:10:00", "timeStep": 30,"offSet":0}

# boundaryControl
boundary01 = [
    [
        "U_Coupled02",
        "U",
        "J4",
        {"model": "SWMM"},
    ]
]
boundary011 = [
    [
        "U_Coupled02",
        "p",
        "Out1",
        {"model": "SWMM"},
    ]
]
boundary022 = [
    [
        "U_Coupled02",
        "p",
        "movingWall",
        {"model": "OpenFOAM"},
    ]
]
boundary02 = [
    [
        "U_Coupled02",
        "U",
        "inlet",
        {"model": "OpenFOAM"},
    ]
]

# Cases
## SWMM
case01 = {
    "model": "SWMM",
    "name": "swmm.inp",
    "timeControl": timeControl1,
    "boundaryControl": boundary01,
}

## OpenFOAM
case02 = {
    "model": "OpenFOAM",
    "name": "pipe1",
    "timeControl": timeControl,
    "boundaryControl": boundary02,
}
case022 = {
    "model": "OpenFOAM",
    "name": "cavity",
    "timeControl": timeControl,
    "boundaryControl": boundary02,
}
case03 = {
    "model": "OpenFOAM",
    "name": "cavitycc",
    "timeControl": timeControl,
    "boundaryControl": boundary02,
}

# Sequence of cases running
cases = [case01, case02]
