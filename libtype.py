import pandas as pd
import re

def removeblank(scalar):
    if scalar=='':
        return float(1.0) 
    else:
        return scalar

def getvalue(strwithnum):
    if type(strwithnum) is str:
        return float(re.findall(r"\((\d+.\d+).\)",strwithnum)[0])
    else:
	    raise ValueError(f"Unusual content '{strwithnum}'")

def getflatnum(scalar):
    if isinstance(scalar,str):
        try:
            return int(scalar)
        except:
            print(f"{scalar} is a literal cannot be typed to float")
            return scalar
    elif isinstance(scalar,(int,float)):
        return float(scalar)
    else:
        raise TypeError(f"Unusual input scalar '{scalar}'")

def isaudit(frame):
    frame=pd.read_excel(frame,nrows=5)
    if frame.shape[1]==16:
        return "audit"
    else:
        return "zakup"

def occdiv(object,factor):
    '''
    Divide by occurance.
    '''
    object=float(object)
    return round(object/(int(factor)//1),5)

def occdivstats(frame):
    '''
    Divide mean-based stats in a frame
    '''
    #Check basis type
    meanStat=['EPS','EPH','JPH']
    if 'complyRate' in frame.columns:
        meanStat+=['complyRate']
    if 'auditRate' in frame.columns:
        meanStat+=['auditRate']
    #Should be divided by factor or 'occurance//1'
    for i in frame.index:
        factor=frame.loc[i,"occurance"]
        if factor>1:
            for h in meanStat:
                frame.loc[i,h]=occdiv(frame.loc[i,h],factor)
    return frame

def meaning(objectsum,objectlen):
    if objectlen==0:
        objectlen=1
    try:
        return objectsum/(objectlen//1)
    except TypeError:
        raise ZeroDivisionError(f"Foremost argument '{objectsum}' is 0")

def dashingcn(object):
    if type(object) is not str:
        object=str(object)
        object.replace("-","")
        return "-".join([object[:6],object[6:]])
    else:
        print(f"Substitution failed for '{object}'")
        return "910117-1932416"

def dashingpn(object):
    if type(object) is not str:
        object=str(object)
    object.replace("-","")
    if len(object)!=11:
        if len(object)==9:
            object="0"+object+"0"
        elif len(object)==10:
            object="0"+object
        else:
            print(f"Substitution failed for '{object}'")
            return "010-9405-6485"
    return "-".join([object[:3],object[3:7],object[7:]])

def jobcoding(object):
    if isinstance(object,str)!=True:
        try:
            return int(str(object).strip())
        except:
            print(f"Substitution failed for '{object}'")
            return 61394
    elif isinstance(object,(float,int)):
        return int(object)