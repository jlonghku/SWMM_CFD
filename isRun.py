import para, checkState as ck
def isRun(dirs,init,sw_time,of_time):
    islock=ck.checkState(dirs)
    if (islock==False)&(init==1)&(sw_time<=of_time):
        return 1
    elif (islock==False)&(init==1)&(sw_time>of_time) :
        return 2
    elif (islock==False)&(init==0)&(sw_time<of_time):
        return 1
    elif (islock==False)&(init==0)&(sw_time>=of_time):
        return 2
    else:
        return 3       