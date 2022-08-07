import pandas as pd
from datetime import datetime as dt

class etp:
    def __init__(self,type,lq,bv0,bv1,etc,name="etp"):
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
    def vwp(alpha,beta,delta):
        return "vwap"

def pro(cap):
    q=cap/10
    w=q*2
    e=w*2
    r=q*5
    return {
        "10":q,
        "20":w,
        "40":e,
        "50":r}
def messij():
    pass
def sig(startingFrom):
    startingFrom=pd.Timestamp(startingFrom)
    ima=pd.Timestamp(dt.now())
    delta=ima-startingFrom
    print(f"{delta=}")
    return f"{(delta.components.hours*60)+delta.components.minutes}"