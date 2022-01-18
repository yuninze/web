import pandas as pd
import re,os

def getvalue(strwithnum):
    if type(strwithnum) is str:
        return float(re.findall(r"\((\d+.\d+).\)",strwithnum)[0])
    else:
	    raise ValueError("Unusual content")

def isaudit(frame):
    frame=pd.read_excel(frame,nrows=5)
    if frame.shape[1]==16:
        return "audit"
    else:
        return "work"

def meaning(objectsum,objectlen):
    objectlen=objectlen//1
    return objectsum/objectlen

def dashingcn(object):
    if type(object) is not str:
        object=str(object)
        object.replace("-","")
        return "-".join([object[:6],object[6:]])
    else:
        return "입력거부"

def dashingpn(object):
    if type(object) is not str:
        object=str(object)
    if len(object)!=11:
        if len(object)==9:
            object="0"+object+"0"
        elif len(object)==10:
            object="0"+object
        else:
            return "010-9405-6485"
    object.replace("-","")
    return "-".join([object[:3],object[3:7],object[7:]])

def jobcoding(object):
    try:
        int(object)
        return str(object)
    except:
        return "777"

def purify(target,danga=10):
    if isaudit(target)=="audit":
        cols=["id","mail","name","nick","work","complianceRate","TWT"]
        usecols="A,B,C,D,F,I,K"
        frame=pd.read_excel(target,usecols=usecols,na_filter=True).drop([0])
        frame.columns=cols
        frame.complianceRate=frame.complianceRate.apply(float)
    elif isaudit(target)=="work":
        cols=["id","mail","name","nick","work","auditRate","TWT"]
        usecols="A,B,C,D,E,L,N"
        frame=pd.read_excel(target,usecols=usecols,na_filter=True).drop([0])
        frame.columns=cols
        frame.auditRate=frame.auditRate.apply(float)
    else:
        raise IndexError("Unusual frame")
    #Set integer id as index
    frame.id=frame.id.apply(int)
    frame.set_index("id",inplace=True)
    #Tries to parse TWT to float
    frame.TWT=frame.TWT.apply(getvalue)
    #Results stats
    for i in frame.index:
        ii=list(frame.index).index(i)
        if frame.loc[i,"TWT"]>0:
            frame.loc[i,"TE"]=frame.iloc[ii,3]*danga
            frame.loc[i,"TE1000"]=frame.loc[i,"TE"]/1000
            frame.loc[i,"EPS"]=frame.loc[i,"TE"]/frame.loc[i,"TWT"]
            frame.loc[i,"EPH"]=(frame.loc[i,"TE"]/frame.loc[i,"TWT"])*3600
            frame.loc[i,"JPH"]=3600/(frame.loc[i,"TWT"]/frame.iloc[ii,3])
    #Sanitizes index to prepare concatnating
    frame.reset_index(inplace=True)
    frame.set_index(["id","mail","name","nick"],inplace=True)
    return frame

#Unconditional concatenating
frame=pd.concat([a,b,c,d,e,f],axis=0)
#Groupbying
frame=frame.groupby(by=frame.index.names)
#Transforming
frame=frame.transform("sum")
#Aggregate index counts
frame.loc[:,"occurance"]=frame.index.value_counts()
#Remove duplicated indexes
frame.reset_index(inplace=True)
frame.drop_duplicates(subset=["id","mail","name","nick"],inplace=True)
frame.set_index(["id","mail","name","nick"],inplace=True)

#Dividing by occurance, target, factor (occurance//1)
def occdiv(object,factor):
    if isinstance(object,(int,float)):
        pass
    else:
        object=float(object)
    if isinstance(factor,(int,float)):
        factor=int(factor)//1
    else:
        factor=int(factor)//1
    return round(object/factor,5)
#Mean-based stats should be divided by factor or 'occurance//1'
for i in frame.index:
    factor=frame.loc[i,"occurance"]
    if factor!=1:
        for h in ('EPS','EPH','JPH'):
            frame.loc[i,h]=occdiv(frame.loc[i,h],factor)
#Sanitize temp columns
frame.drop("occurance",axis=1,inplace=True)

#Index sanitization for pii merging
frame.reset_index(inplace=True)
frame.drop(["nick","id"],axis=1,inplace=True)
frame.set_index(["mail","name"],inplace=True)
