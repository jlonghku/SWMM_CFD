def getOfTime(dirs):
    import os
    os.system('foamListTimes -case openfoam >of_timelist.log')
    with open("of_timelist.log") as f:
        lines=f.readlines()
        if lines==[]:
            of_time=0
        else:  
            of_time=float(lines[-1])
    return of_time