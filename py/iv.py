from pandas import Timestamp as ts
from time import time
from datetime import datetime

class etp:
    def __init__(self,
    type,lq,bv0,bv1,etc,name="etp"):
        self.name=name
        self.type=type
        self.lq=lq
        self.bv0=bv0
        self.bv1=bv1
        self.etc=etc

    def iv(self):
        delta=abs(self.bv1-self.bv0)/self.bv0
        if type>0:
            basis=1+delta
        else:
            basis=1-delta
        diff=self.lq*(basis-1)
        iv=(self.lq*basis)*(1-(self.etc/365))
        print((self.lq,
            self.bv0,
            self.bv1,
            self.etc,round(self.etc/365,5)))
        return {"delta":delta,
            "difference":diff,
            "iv":iv}

def now():
    print(datetime.now().strftime("%Y-%m-%d %H:%M"))
    return time()

def wrk(t0,ts=None):
    t1=time()
    if not ts:
        return (t1-t0)//60
    return ((t1-t0)//60)-ts