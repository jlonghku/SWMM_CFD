# import input file
import para

# import runModel Control
from runModel import runModel

# import special model's module
runModel.clsImportModels(['OpenFOAM']) 

# inital the runModel class
runModel.clsInit(para)

# run subCases
runModel.clsRun()
