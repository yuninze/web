import re
import pandas as pd
enc="utf-8-sig"

def purify0(fileObjectName):
    """
    Unconditionally converts a DP-derived sheetfile into
    a csvfile with sanitized name of columns and data-types.

    Returns:: Csvfile
    """
    if ".xlsx" in fileObjectName:
        fileObject=pd.read_excel(fileObjectName,na_filter=False)
        str(fileObjectName).replace("xlsx","csv")
        fileObject.to_csv(fileObjectName,index=False,encoding=enc)
        df=pd.read_csv(fileObjectName,encoding=enc).reset_index()
    elif ".csv" in fileObjectName:
        df=pd.read_csv(fileObjectName,encoding=enc).reset_index()
    if len(df.columns)==4:
        df.columns=["pid","name","mail","count0"]
    elif len(df.columns)==5:
        df.columns=["pid","name","mail","count0","count1"]
    df.pid=df.pid.apply(int)
    return df

def ta0(fileObjectName):
    """
    Based on complicated multi-indexes,
    convert columns into per-index stacked rows.
    converted per-index stacked rows would be
    a new component of multi-indexes.
    Unsatisfying values in the dataframe turned into NaN.

    Returns::: DataFrame
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
    return df.set_index(["pid","mail","name"]).stack()

def purify2(fo):
    """
    TA Hyunbum sheet

    Returns::: DataFrame
    """
    try:
        u=pd.read_excel(fo+".xlsx",na_filter=False)
    except:
        try:
            u=pd.read_csv(fo+".csv",encoding="utf-8")
        except:
            u=pd.read_csv(fo+".csv",encoding="utf-8-sig")
    u.columns=[
        "date","name","mail","phone","cn","cn0","loc","edu",
        "job","zangae","preg","gzy","bohun","damunwha",
        "choding","daeding",
        "jobtwo","jobno","jobloss","lowincome","jobless",
        "mobuzang","visamarry","bukhan","selfempoly",
        "aihubHx","icHx","consent0","consent1"
    ]
    u.drop(["consent0","consent1","date","cn0"],axis=1,inplace=True)
    u.drop_duplicates(subset=["name","mail"],inplace=True)
    #u.set_index("name",inplace=True)
    u.loc[:,["name","mail","cn","phone"]]=u.loc[:,["name","mail","cn","phone"]].applymap(lambda a:str(a).strip())
    for x in u.index:
        if len(u.loc[x,"phone"])==9:
            u.loc[x,"phone"]="0"+u.loc[x,"phone"]+"0"
        elif len(u.loc[x,"phone"])==10:
            u.loc[x,"phone"]="0"+u.loc[x,"phone"]
    u.cn=u.cn.apply(lambda a:"-".join([a[:6],a[6:]]))
    u.phone=u.phone.apply(lambda x:"-".join((x[:3],x[3:7],x[7:])))
    return u

def purifyboa(fo,danga):
    """
    Results sanitized dataframe from BO-derived sheetfile,
    with additional stats regarding of danga.
    
    Returns:::Dataframe
    """
    udf=pd.read_excel(fo,usecols="A,B,F,I,K",na_filter=False).drop([0])
    udf.columns=[
    "id","mail",
    "allFinished","compliance",
    "TWT"]
    udf.set_index("id",inplace=True)
    udf.index=udf.index.map(int)
    def GetValInSec(object):
        if type(object)==str:
            pass
        else:
            object=str(object)
        return float(re.findall(r"\((\d+.\d+).\)",object)[0])
    udf.TWT=udf.TWT.apply(GetValInSec)
    udf.loc[:,"allFinished":]=udf.loc[:,"allFinished":].applymap(float)
    udf["EPS"]=0
    udf["EPH"]=0
    for c in udf.index:
        if udf.loc[c,"TWT"]>0:
            udf.loc[c,"TE"]=udf.loc[c,"allFinished"]*danga
            udf.loc[c,"TE1000"]=(udf.loc[c,"allFinished"]*danga)/1000
            udf.loc[c,"EPS"]=(danga*udf.loc[c,"allFinished"])/(udf.loc[c,"TWT"])
            udf.loc[c,"EPH"]=udf.loc[c,"EPS"]*3600
            udf.loc[c,"JPH"]=(udf.loc[c,"TWT"]/udf.loc[c,"allFinished"])/3600
        else:
            udf.loc[c,"EPS"]=sum(udf.EPS)/len(udf.EPS)
            udf.loc[c,"EPH"]=sum(udf.EPH)/len(udf.EPH)
    def sex(number):
        return round(number,4)
    udf.loc[:,"allFinished":]=udf.loc[:,"allFinished":].applymap(sex)
    return udf

def purifyboz(fo,danga):
    """
    Results sanitized dataframe from BO-derived sheetfile,
    with additional stats regarding of danga.
    
    Returns:::Dataframe
    """
    udf=pd.read_excel(fo,usecols="A:I,K,L,N:P",na_filter=False).drop([0])
    udf.columns=[
        "id","mail","name","nick",
        "work","audit","reaudit","audited","allFinished","dispute","disputeRate",
        "TWT","WTPJ","WTPJB"]
    udf.drop(["name","nick"],axis=1,inplace=True)
    udf.set_index("id").dropna(axis=0,inplace=True)
    udf.index=udf.index.map(int)
    for t in range(len(udf.index)):
        for s in [udf.TWT,udf.WTPJ]:
            s.iloc[t]=re.findall(r"\((\d+.\d+).\)",s.iloc[t])[0]
    udf.loc[:,"work":]=udf.loc[:,"work":].applymap(lambda fuck:float(fuck))
    udf["EPS"]=0
    udf["EPH"]=0
    for c in udf.index:
        if udf.loc[c,"TWT"]>0:
            udf.loc[c,"TE"]=udf.loc[c,"work"]*danga
            udf.loc[c,"TE1000"]=(udf.loc[c,"work"]*danga)/1000
            udf.loc[c,"EPS"]=(danga*udf.loc[c,"work"])/udf.loc[c,"TWT"]
            udf.loc[c,"EPH"]=udf.loc[c,"EPS"]*3600
            udf.loc[c,"JPH"]=udf.loc[c,"WTPJ"]/3600
        else:
            udf.loc[c,"EPS"]=sum(udf.EPS)/len(udf.EPS)
            udf.loc[c,"EPH"]=sum(udf.EPH)/len(udf.EPH)
    def fuck(number):
        return round(number,4)
    udf.loc[:,"WTPJ":]=udf.loc[:,"WTPJ":].applymap(fuck)
    return udf

def GetNumInSec(object):
    try:
        if type(object) is not str:
            object=str(object)
            return float(re.findall(r"\((\d+.\d+).\)",object)[0])
    except:
        return "RITCHRD"

def GetNumInMean(objectsum,objectlen):
    objectlen=objectlen//1
    return objectsum/objectlen

def GetValInSec(object):
    try:
        if type(object) is not str:
            object=str(object)
            return float(re.findall(r"\((\d+.\d+).\)",object)[0])
    except:
        return "strange"

def CnDashing(object):
    if type(object) is not str:
        object=str(object)
    object.replace("-","")
    return "-".join([object[:6],object[6:]])

def PnDashing(object):
    if type(object) is not str:
        object=str(object)
    object.replace("-","")
    return "-".join([x[:3],x[3:7],x[7:]])

d[
        "zangae","preg","gzy","bohun","damunwha",
        "choding","daeding",
        "jobtwo","jobno","jobloss","lowincome","jobless",
        "mobuzang","visamarry","bukhan","selfempoly",
        "aihubhx","ichx"]=None

for x in d.index:
    row=d.loc[x,"variety"]
    if "장애" in row:
        d.loc[x,"zangae"]="O"
    elif "임신" in row:
        d.loc[x,"preg"]="O"
    elif "단절" in row:
        d.loc[x,"gzy"]="O"
    elif "보훈" in row:
        d.loc[x,"bohun"]="O"
    elif "다문화" in row:
        d.loc[x,"damunwha"]="O"
    elif "초등" in row:
        d.loc[x,"choding"]="O"
    elif "대학생" in row:
        d.loc[x,"daeding"]="O"
    elif "투잡" in row:
        d.loc[x,"jobtwo"]="O"
    elif "미취업자" in row:
        d.loc[x,"jobno"]="O"
    elif "실직자" in row:
        d.loc[x,"jobloss"]="O"
    elif "저소득" in row:
        d.loc[x,"lowincome"]="O"
    elif "장기실업" in row:
        d.loc[x,"jobless"]="O"
    elif "가장" in row:
        d.loc[x,"mobuzang"]="O"
    elif "이주" in row:
        d.loc[x,"visamarry"]="O"
    elif "북한" in row:
        d.loc[x,"bukhan"]="O"
    elif "자영업" in row:
        d.loc[x,"selfempoly"]="O"
    elif "AI" in row:
        d.loc[x,"aihubhx"]="O"

def DivisionByOccurance(object,occurance):
    if type(occurance) is not int:
        occurance=occurance//1
    elif type(object) is not float:
        object=float(object)
    else:
        pass
    return round(object/occurance,4)

TargetObjects=["WTPJ","WTPJB","EPS","EPH","JPH"]
for x in df.index:
    factor=df.loc[x,"occurance"]
    for y in TargetObjects:
        df.loc[x,y]=DivisionByOccurance(df.loc[x,y],factor)
    
def NanToStr(object):
    if type(object) is not str:
        try:
            return str(object)
        except:
            return object
    else:
        return object

def ForcedJobCoding(object):
    try:
        int(object)
        return str(object)
    except:
        return "0"

def queuing():
arc=ZipFile(zipfile,"r")
infolist=arc.infolist()
arcnamelist=[infolist[x] for x in range(len(infolist)) if infolist[x].endswith(".jpg")]

factor=2000

blockcount=len(donefilename)//factor
blocknumber=len(donefilename)%factor
blockindex=0

donefilenamelist=[]
donefilenameblock=dict()

for x in range(blockSize)
    [blockindex:blockcontent for blockindex,blockcontent in range(blockcount),[donefilenamelist for x in range(blockSize 



bo["perf"]=None
CEs={"CEa":None,"CEb":None,"CEc":None,"CEd":None,"CEe":None,"CEf":None,"CEg":None}
CSs={"work":None,"audit":None,"dr":None,"wt":None,"wtPerWork":None,"wtBasis":None}
for z in bo.index:
    for y in bo.loc[z,"mail"]:
        if "naver.com" in y:
            CEs["CEa"]=0.9
        elif "nate.com" in y:
            CEs["CEa"]=0.7
        elif "hanmail.net" in y:
            CEs["CEa"]=0.8
        elif "daum.net" in y:
            CEs["CEa"]=0.7
        elif "gmail.com" in y:
            CEs["CEa"]=1.1
        elif "hotmail.com" in y:
            CEs["CEa"]=0.6
        else:
            CEs["CEa"]=0.9