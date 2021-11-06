# SWMM_CFD
Model coupling SWMM and OpenFOAM
## Installation
The tool is designed to run under Linux operating system, where Ubuntu 18.04 and 20.04 are recommended. It contains a self-extracting setup script. To install it:
1. Select a path where you want to install it and use the below commands in this path
2. Download the package by command:
“git clone https://github.com/jlonghku/SWMM_CFD ”
3. Change the permission of package: “sudo chmod 755 -R SWMM_CFD”
4. Run the “install.sh” script file in the file directory downloaded: “./SWMM_CFD /install.sh”
## General steps of model operation
The following are the most common steps for using this model:
1. Prepare the SWMM case input file by the GUI of EPA SWMM.
2. Prepare the OpenFOAM case by modifying the parameters on the example provided in directory “tut” or customizing new cases according to study.
3. Organize all SWMM and OpenFOAM cases into a folder according to template provided. 
4. Add the control file into the case and modify parameters inside.
5. Run the cases by command.
6. View or post-processing the results of the simulation.
For a quick start of a sample case, please refer to Section 2 in manual. For more settings of different control files, please refer to Section 3 in manual of setting up different case files.

We provide some example cases in the directionary SWMM_CFD/Case. A quick start command of the sample 1:
```python
python3 main.py
```

For more details, please see the user's manual. 

