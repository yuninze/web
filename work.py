import re,os,math
import pandas as pd
from pandas.core.indexes.multi import MultiIndex
enc="utf-8-sig"

def GetNumInSec(object):
    if type(object) is str:
        if len(object)<8:
            return 1.1
        else:
            return float(re.findall(r"\((\d+.\d+).\)",object)[0])
    elif math.isnan(object):
        return 1.1

def GetNumInMean(objectsum,objectlen):
    objectlen=objectlen//1
    return objectsum/objectlen

def DivisionByOccurance(object,occurance):
    if isinstance(object,(int,float)):
        pass
    else:
        object=float(object)
    if isinstance(occurance,(int,float)):
        occurance=occurance//1
    else:
        occurance=int(occurance)
    return round(object/occurance,5)

def CnDashing(object):
    if type(object) is not str:
        object=str(object)
    object.replace("-","")
    return "-".join([object[:6],object[6:]])

def PnDashing(object):
    if type(object) is not str:
        object=str(object)
    object.replace("-","")
    return "-".join([object[:3],object[3:7],object[7:]])

def NanToStr(object):
    if type(object) is not str:
        try:
            return str(object)
        except:
            return object
    else:
        return object

def sex(number):
    if type(number) is float:
        return round(number,5)
    else:
        return number

def ForcingJobCode(object):
    try:
        int(object)
        return str(object)
    except:
        return "101010"

def IsAudit(dataFrameAlikeObject):
    """
    Check Whether DataFrame is Audit or Work.

    Results 0: Work or 1: Audit
    """
    dataframe=pd.read_excel(dataFrameAlikeObject,nrows=5)
    if dataframe.shape[0]!=16:
        return 0 or 1

def ta0(fileObjectName):
    """
    Based on complicated multi-indexes,
    convert columns into per-index stacked rows.
    converted per-index stacked rows would be
    a new component of multi-indexes.
    """
    df=pd.read_csv(fileObjectName,encoding=enc).reset_index()
    colnum=len(df.columns)
    try:
        df.set_index(["pid","mail","name"],inplace=False)
    except:
        assert NotImplementedError("Multi-index element not percieved")
    if colnum==4:
        df["count0t"]=df.groupby(["pid","mail","name"])["count0"].transform("sum")
    elif colnum==5:
        df["count0t"]=df.groupby(["pid","mail","name"])["count0"].transform("sum")
        df["count1t"]=df.groupby(["pid","mail","name"])["count1"].transform("sum")
    else:
        assert IndexError("FileObject is irrelevant to DETA")
    return df.set_index(["pid","mail","name"]).stack(dropna=True)

def HbToNia(fileObjectName):
    """
    TA Hyunbum sheet
    """
    try:
        u=pd.read_excel(fileObjectName+".xlsx",na_filter=False)
    except:
        try:
            u=pd.read_csv(fileObjectName+".csv",encoding="utf-8")
        except:
            u=pd.read_csv(fileObjectName+".csv",encoding="utf-8-sig")
    u.columns=[
    "date","name","mail","phone","cn","cn0","loc","edu",
    "job","zangae","preg","gzy","bohun","damunwha",
    "choding","daeding",
    "jobtwo","jobno","jobloss","lowincome","jobless",
    "mobuzang","visamarry","bukhan","selfempoly",
    "aihubHx","icHx","consent0","consent1"]
    u.drop(["consent0","consent1","date","cn0"],axis=1,inplace=True)
    u.drop_duplicates(subset=["name","mail"],inplace=True)
    #u.set_index("name",inplace=True)
    u.loc[:,["name","mail","cn","phone"]]=u.loc[
    :,["name","mail","cn","phone"]].applymap(lambda a:str(a).strip())
    for x in u.index:
        if len(u.loc[x,"phone"])!=11:
            if len(u.loc[x,"phone"])==9:
                u.loc[x,"phone"]="0"+u.loc[x,"phone"]+"0"
            elif len(u.loc[x,"phone"])==10:
                u.loc[x,"phone"]="0"+u.loc[x,"phone"]
        else:
            pass
    u.cn=u.cn.apply(CnDashing)
    u.phone=u.phone.apply(PnDashing)
    return u

def purifya(fo,danga):
    """
    Results sanitized dataframe from BO-derived sheetfile,
    with additional stats regarding of danga.
    """
    udf=pd.read_excel(fo,usecols="A,B,F,I,K",na_filter=False).drop([0])
    udf.columns=[
    "id","mail",
    "work","compliance",
    "TWT"]
    udf.set_index("id",inplace=True)
    udf.index=udf.index.map(int)
    udf.TWT=udf.TWT.apply(GetNumInSec)
    print(udf.TWT)
    udf.loc[:,"work":]=udf.loc[:,"work":].applymap(float)
    udf["EPS"],udf["EPH"]=0,0
    for x in udf.index:
        if udf.loc[x,"TWT"]>0:
            udf.loc[x,"TE"]=udf.loc[x,"work"]*danga
            udf.loc[x,"TE1000"]=(udf.loc[x,"work"]*danga)/1000
            udf.loc[x,"EPS"]=udf.loc[x,"TE"]/udf.loc[x,"TWT"]
            udf.loc[x,"EPH"]=udf.loc[x,"EPS"]*3600
            udf.loc[x,"JPH"]=(udf.loc[x,"TWT"]/udf.loc[x,"work"])/3600
        else:
            udf.loc[x,"EPS"]=sum(udf.EPS)/len(udf.EPS)
            udf.loc[x,"EPH"]=sum(udf.EPH)/len(udf.EPH)
    udf.loc[:,"work":]=udf.loc[:,"work":].applymap(sex)
    return udf.reset_index()

def purifyz(fo,danga):
    """
    Results sanitized dataframe from BO-derived sheetfile,
    with additional stats regarding of danga.
    """
    udf=pd.read_excel(fo,usecols="A:I,K,L,N:P",na_filter=False).drop([0])
    udf.columns=[
    "id","mail","name","nick",
    "work","audit","reaudit","audited","AF","dispute","disputeRate",
    "TWT","WTPJ","WTPJB"]
    udf.drop(["name","nick"],axis=1,inplace=True)
    udf.set_index("id").dropna(axis=0,inplace=True)
    udf.index=udf.index.map(int)
    udf.loc[:,["TWT","WTPJ"]]=udf.loc[:,["TWT","WTPJ"]].applymap(GetNumInSec)
    print(udf.TWT)
    udf.loc[:,"work":]=udf.loc[:,"work":].applymap(float)
    udf["EPS"],udf["EPH"]=0,0
    for c in udf.index:
        if udf.loc[c,"TWT"]>0:
            udf.loc[c,"TE"]=udf.loc[c,"work"]*danga
            udf.loc[c,"TE1000"]=(udf.loc[c,"work"]*danga)/1000
            udf.loc[c,"EPS"]=(danga*udf.loc[c,"work"])/udf.loc[c,"TWT"]
            udf.loc[c,"EPH"]=udf.loc[c,"EPS"]*360
            udf.loc[c,"JPH"]=udf.loc[c,"WTPJ"]/3600
        else:
            udf.loc[c,"EPS"]=sum(udf.EPS)/len(udf.EPS)
            udf.loc[c,"EPH"]=sum(udf.EPH)/len(udf.EPH)
    def fuck(number):
        return round(number,4)
    udf.loc[:,"WTPJ":]=udf.loc[:,"WTPJ":].applymap(fuck)
    return udf.reset_index()

def fuckfuck(zdanga,adanga,path="c:/"):
    """
    Concatenate, group, aggregate sheets in path.

    Always uses ["id","mail"] as index.
    """
    if zdanga<1:
        zdanga=10
    if adanga<1:
        adanga=10
    fuck=(path+x for x in os.listdir(path) if x.endswith(".xls"))
    idx=["id","mail"]
    cols=["EPS","EPH","JPH"]
    audit,zakup={},{}
    for x in fuck:
        if IsAudit(x):
            audit[x]=purifya(x,adanga)
        else:
            zakup[x]=purifyz(x,zdanga)
    cache=[]
    for frames in (audit,zakup):
        if len(frames)==0:
            continue
        frame=[v.set_index(idx,inplace=True) for v in frames.values()]
        frame=pd.concat(frames.values())
        frameOrgIdx=frame.index
        frame.work=frame.work.apply(int)
        frame.TWT=frame.TWT.apply(float)
        #print(frame)
        try:
            frame=frame.groupby(level=frame.index.names)
        except:
            raise IndexError(f"Groupbying by {idx} failed")
        finally:
            #Get count of each multiindexes
            frameIdxLen=frameOrgIdx.value_counts()
            frameIdxLen.name="occurance"
            frameIdxLen.index=MultiIndex.from_tuples(frameIdxLen.index,names=idx)
            frame=frame.sum()
            if len(frame.index)==len(frameOrgIdx):
                raise IndexError("Analoguous index length")
            if len(frameIdxLen.index)!=len(frame.index):
                raise IndexError(
                f"Index length mismatch ({len(frameIdxLen)}:{len(frame.index)})")
            frame=frame.merge(frameIdxLen,left_index=True,right_index=True)
            #Divide average stats columns by occurnace
            for x in frame.index:
                factor=frame.loc[x,"occurance"]
                if frames is audit:
                    pass
                elif frames is zakup:
                    cols+=["WTPJ","WTPJB"]
                for y in cols:
                    frame.loc[x,y]=DivisionByOccurance(frame.loc[x,y],factor)
        #Load the final product
        cache+=[frame.drop("occurance",axis=1)]
    return cache