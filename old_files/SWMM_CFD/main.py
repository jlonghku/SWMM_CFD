# import sys,importlib
# # import input data for coupling models
# para = importlib.import_module(str(sys.argv[1]))
import para

# import runModel Control
from runModel import runModel

# import special model's module (the .py file name), can be custom-designed module
runModel.clsImportModels(["OpenFOAM", "SWMM"])

# inital the runModel class with parameters
runModel.clsInit(para)

# run Cases
runModel.clsRun()

