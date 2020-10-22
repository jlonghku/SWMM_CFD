import numpy as np
import re
def read_data(dataname):
    with open(dataname) as f:
        next(f)
        p1=0.0
        flux=0.0
        for line in f:
            tp = re.compile(r'[(](.*?)[)]')
            p=re.split(tp,line)
            p0=list(filter(lambda s: s and (type(s) != str or len(s.strip()) > 0), p))
            p1=float(p0[0])
            p2=np.fromstring(p0[1],dtype='float',sep=' ') 
            p3=np.fromstring(p0[2],dtype='float',sep=' ') 
            flux+=p1*np.dot(p2,p3)
        print(flux)
    return flux