import pandas as pd
import numpy as np
import re

def removeblank(scalar):
    if scalar=='':
        return 1
    else:
        return scalar

def flat(scalar):
    try:
        return np.float32(scalar)
    except:
        if isinstance(scalar,str):
            print(f"'{scalar}' is a literal cannot be typed to float")
            return scalar
        else:
            raise TypeError(f"'{scalar}' is neither of str or number")

def getvalue(strwithnum):
    if isinstance(strwithnum,str):
        return re.findall(r"\((\d+.\d+).\)",strwithnum)[0]
    else:
	    raise ValueError(f"Unusual scalar '{strwithnum}'")

def isaudit(frame):
    frame=pd.read_excel(frame,nrows=5)
    if frame.shape[1]==16:
        return 1
    else:
        return 0

def occdiv(frame):
    #check basis type
    meanstat=['EPS','EPH','JPH']
    if 'complyRate' in frame.columns:
        meanstat+=['complyRate']
    if 'auditRate' in frame.columns:
        meanstat+=['auditRate']
    #divide by occurance
    for i in frame.index:
        factor=frame.loc[i,'occurance']//1
        stat=frame.loc[i,meanstat]
        frame.loc[i,meanstat]=frame.loc[i,meanstat]/factor
    return frame

def meaning(scalarsum,scalarlen):
    if scalarsum==0:
        scalarsum=1
    try:
        return scalarsum/(scalarlen//1)
    except TypeError:
        raise ZeroDivisionError(f"Foremost argument '{scalarsum}' is 0")

def dashingcn(object):
    if isinstance(object,str)==False:
        object=str(object)
        object.replace("-","")
        return "-".join([object[:6],object[6:]])
    else:
        print(f"Substitution failed for '{object}'")
        return "910117-1932416"

def dashingpn(object):
    if isinstance(object,str)==False:
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

def accountingtostr(scalar):
    return str(scalar).replace(',','')

def jobcoding(object):
    if isinstance(object,str)==False:
        try:
            return int(str(object).strip())
        except:
            print(f"Substitution failed '{object}'")
            return 61394
    elif isinstance(object,(float,int)):
        return int(object)

def occdivx(object,factor):
    return object/(factor//1)