import pandas as pd
import re,os,math

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
            print(f"{scalar} is a literal cannot be typed to a float")
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
    object=float(object)
    return round(object/(int(factor)//1),5)

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

def purify(target,danga=10):
    #Purifying setting upon isaudit
    if isaudit(target)=="audit":
        basis="complyRate"
        cols=["id","mail","name","nick","work",basis,"TWT"]
        usecols="A,B,C,D,F,I,K"
    elif isaudit(target)=="zakup":
        basis="auditRate"
        cols=["id","mail","name","nick","work",basis,"TWT"]
        usecols="A,B,C,D,E,L,N"
    else:
        raise IndexError("Unusual frame columns")
    #Attempt to load within settings above
    frame=pd.read_excel(target,usecols=usecols,na_filter=True).drop([0])
    frame.columns=cols
    #Fill NaN and null
    frame=frame.applymap(removeblank)
    #Type basisRate
    frame[basis]=frame[basis].apply(float)
    #Set id as integer
    frame.id=frame.id.apply(int)
    frame.set_index("id",inplace=True)
    #Try to parsing TWT to float
    frame.TWT=frame.TWT.apply(getvalue)
    #Regards zero work count
    frame.work=frame.work.apply(getflatnum)
    #Result stats
    for i in frame.index:
        if frame.loc[i,"TWT"]>0:
            frame.loc[i,"TE"]=(frame.loc[i,"work"]*danga)
            frame.loc[i,"TE1000"]=(frame.loc[i,"work"]*danga)/1000
            frame.loc[i,"EPS"]=((frame.loc[i,"work"]*danga)/frame.loc[i,"TWT"])
            frame.loc[i,"EPH"]=((frame.loc[i,"work"]*danga)/frame.loc[i,"TWT"])*3600
            if frame.loc[i,"work"]<1:
                frame.loc[i,"work"]=meaning(sum(frame.loc[:,"work"]),len(frame.loc[:,"work"]))
                frame.loc[i,"TWT"]=meaning(sum(frame.loc[:,"TWT"]),len(frame.loc[:,"TWT"]))
                frame.loc[i,"JPH"]=3600/(frame.loc[i,"TWT"]/frame.loc[i,"work"])
            else:
                frame.loc[i,"JPH"]=3600/(frame.loc[i,"TWT"]/frame.loc[i,"work"])
    #Sanitize index to concatnating
    frame.reset_index(inplace=True)
    frame.set_index(["id","mail","name","nick"],inplace=True)
    return [frame,basis]

def concoction(path,auditDanga,zakupDanga):
    #framefileObject collection with pathstring
    sheetfiles=[path+"/"+z for z in os.listdir(path) if ".xls" in z]
    frames={}
    #Confirm whether frame type
    for framename in sheetfiles:
        if isaudit(framename)=="zakup":
            danga=zakupDanga
        elif isaudit(framename)=="audit":
            danga=auditDanga
        #Purify upon frame type
        frames[framename]=purify(framename,danga)[0]
    #Unconditional concatenate
    frame=pd.concat([y for x,y in frames.items()],axis=0,ignore_index=False)
    #Groupby
    frame=frame.groupby(by=frame.index.names)
    #Transform by sum
    frame=frame.transform("sum")
    #Aggregate index occurance
    frame.loc[:,"occurance"]=frame.index.value_counts()
    #Remove index dupes
    frame.reset_index(inplace=True)
    frame.drop_duplicates(subset=["id","mail","name","nick"],inplace=True)
    frame.set_index(["id","mail","name","nick"],inplace=True)
    frame.sort_index(inplace=True)
    #Check basis type
    meanStat=['EPS','EPH','JPH']
    if 'complyRate' in frame.columns:
        meanStat+=['complyRate']
    if 'auditRate' in frame.columns:
        meanStat+=['auditRate']
    #Should be divided by factor or 'occurance//1'
    for i in frame.index:
        factor=frame.loc[i,"occurance"]
        #
        if factor>1:
            for h in meanStat:
                if h in ('complyRate','auditRate'):
                    factor*=2
                    frame.loc[i,h]=occdiv(frame.loc[i,h],factor)
                else:
                    factor*=1
                    frame.loc[i,h]=occdiv(frame.loc[i,h],factor)
    #Sanitize temp columns
    frame.drop("occurance",axis=1,inplace=True)
    #Index sanitization for pii merging
    frame.reset_index(inplace=True)
    frame.drop(["nick","id"],axis=1,inplace=True)
    frame.set_index(["mail","name"],inplace=True)
    #Try to open pii frame
    piipath=path+"/"+"pii.csv"
    try:
        pii=pd.read_csv(piipath).drop("Unnamed: 0",axis=1)
        #Set index by name and mail
        pii.set_index(['mail','name'],inplace=True)
        #Merge by index
        return pii.merge(frame,left_index=True,right_index=True)
    except:
        print(f"'{piipath}' does not exist")
        return frame