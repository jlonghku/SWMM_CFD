# a,b=checkstate('comms/')
def checkState(dirs):
    import os

    if not os.path.exists(dirs):
        os.mkdir(dirs)
    
    islock=False
    files=os.listdir(dirs)
    for i in files:
        arr=i.endswith('lock')
        
        islock=True if arr==True else islock
        

    return islock