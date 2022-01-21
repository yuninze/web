from functools import cache
from operator import index
import pandas as pd
import re,os,math

def removeblank(scalar):
    if type(scalar) is float or int:
        return scalar
    elif pd.isnull(scalar):
        return 1.0
    elif math.isnan(scalar):
        return 1.0
    else:
        return scalar

def getvalue(strwithnum):
    if type(strwithnum) is str:
        return float(re.findall(r"\((\d+.\d+).\)",strwithnum)[0])
    else:
	    raise ValueError(f"Unusual content {strwithnum}")

def getflatnum(scalar):
    if isinstance(scalar,str):
        try:
            return int(scalar)
        except:
            print(f"{scalar} is a literal cannot be typed to a float")
            return scalar
    elif isinstance(scalar,int):
        return float(scalar)
    else:
        raise TypeError(f"Unusual input scalar {scalar}")

def isaudit(frame):
    frame=pd.read_excel(frame,nrows=5)
    if frame.shape[1]==16:
        return "audit"
    else:
        return "zakup"

def occdiv(object,factor):
    if isinstance(object,(int,float)):
        pass
    else:
        object=float(object)
    return round(object/(int(factor)//1),5)

def meaning(objectsum,objectlen):
    if objectlen==0:
        objectlen=1
    try:
        return objectsum/(objectlen//1)
    except TypeError:
        raise ZeroDivisionError(f"Foremost argument {objectsum} is 0")

def dashingcn(object):
    if type(object) is not str:
        object=str(object)
        object.replace("-","")
        return "-".join([object[:6],object[6:]])
    else:
        print(f"Substitution failed for {object}")
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
            print(f"Substitution failed for {object}")
            return "010-9405-6485"
    return "-".join([object[:3],object[3:7],object[7:]])

def jobcoding(object):
    if isinstance(object,str)!=True:
        try:
            return int(str(object).strip())
        except:
            print(f"Substitution failed for {object}")
            return 61394
    elif isinstance(object,(float,int)):
        return int(object)

def purify(target,danga=10):
    #Purifying setting upon isaudit
    if isaudit(target)=="audit":
        cols=["id","mail","name","nick","work","complianceRate","TWT"]
        usecols="A,B,C,D,F,I,K"
        basis="complyRate"
    elif isaudit(target)=="zakup":
        cols=["id","mail","name","nick","work","auditRate","TWT"]
        usecols="A,B,C,D,E,L,N"
        basis="auditRate"
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
            frame.loc[i,"JPH"]=3600/(frame.loc[i,"TWT"]/frame.loc[i,"work"])
    #Sanitize index to concatnating
    frame.reset_index(inplace=True)
    frame.set_index(["id","mail","name","nick"],inplace=True)
    return (frame,basis)

def concoction(path,auditDanga,zakupDanga):
    #framefileObject collection with pathstring
    sheetfiles=[path+z for z in os.listdir(path) if ".xlsx" in z]
    frames={}
    #Confirm whether frame type
    for framename in sheetfiles:
        if isaudit(framename)=="zakup":
            danga=zakupDanga
            basis="complyRate"
        elif isaudit(framename)=="audit":
            danga=auditDanga
            basis="auditRate"
        #Purify upon frame type
        frames[framename]|=purify(framename,danga)[0]
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
    #Mean-based stats should be divided by factor or 'occurance//1'
    for i in frame.index:
        factor=frame.loc[i,"occurance"]
        if factor!=1:
            for h in (basis,'EPS','EPH','JPH'):
                frame.loc[i,h]=occdiv(frame.loc[i,h],factor)
    #Sanitize temp columns
    frame.drop("occurance",axis=1,inplace=True)
    #Index sanitization for pii merging
    frame.reset_index(inplace=True)
    frame.drop(["nick","id"],axis=1,inplace=True)
    frame.set_index(["mail","name"],inplace=True)
    #Try to open pii frame
    try:
        pii=pd.read_csv("pii.csv").drop("Unnamed: 0",axis=1,inplace=True)
    except:
        raise OSError("PII file does not exist")
    #Set index by name and mail
    pii.set_index(['mail','name'],inplace=True)

    

















#Set target columns
targetcols="A,CE,CF,CT,DM"
#Load sheetfile object
a=pd.read_excel("1_82_stats_220118_fromRow282.xlsx",
sheet_name=1,na_filter=False,nrows=4000,usecols=targetcols)
def stringtozero(scalar):
	if isinstance(scalar,str):
		return 0
	elif isinstance(scalar,(int,float)):
		return scalar
#Groupbying, transforming
#Filter dupe indexes only

#Pii to variety
for fuck in d.index:
    col=d.loc[fuck]
    row=col.loc["variety"]
    if "장애" in row:
        col.loc["zangae"]="O"
    elif "임신" in row:
        col.loc["preg"]="O"
    elif "단절" in row:
        col.loc["gzy"]="O"
    elif "보훈" in row:
        col.loc["bohun"]="O"
    elif "다문화" in row:
        col.loc["damunwha"]="O"
    elif "초등" in row:
        col.loc["choding"]="O"
    elif "대학생" in row:
        col.loc["daeding"]="O"
    elif "투잡" in row:
        col.loc["jobtwo"]="O"
    elif "미취업자" in row:
        col.loc["jobno"]="O"
    elif "실직자" in row:
        col.loc["jobloss"]="O"
    elif "저소득" in row:
        col.loc["lowincome"]="O"
    elif "장기실업" in row:
        col.loc["jobless"]="O"
    elif "가장" in row:
        col.loc["mobuzang"]="O"
    elif "이주" in row:
        col.loc["visamarry"]="O"
    elif "북한" in row:
        col.loc["bukhan"]="O"
    elif "자영업" in row:
        col.loc["selfempoly"]="O"
    elif "AI" in row:
        col.loc["aihubhx"]="O"