import os

# Dir
dir = os.path.dirname(os.path.realpath(__file__)) + "/Case"

# timeControl dict
timeControl = {"startTime": "11/01/2017", "endTime": "11/01/2017 00:05:30", "timeStep": 30,"offSet":0}
timeControl1 = {"startTime": 0, "endTime": 120, "timeStep": 30,"offSet":"11/01/2017"}


# boundaryControl
boundary01 = [
    [
        "U_Coupled02",
        "U",
        "J4",
        {"model": "SWMM"},
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
    "timeControl": timeControl,
    "boundaryControl": boundary01,
}

## OpenFOAM
case02 = {
    "model": "OpenFOAM",
    "name": "pipe2",
    "timeControl": timeControl1,
    "boundaryControl": boundary02,
}


# Sequence of cases running
cases = [case01, case02]
