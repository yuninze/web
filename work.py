import os
import re
import pandas as pd
import math


def nurakaud(fo):
    df=pd.read_excel(fo,usecols=["A:D,F"]).reset_index()
    df["by"]=df.groupby(["id"])["포인트적립"].sum()
    df.loc[:,"by"]*10

pd.concat([a,b,c,d,e,f],axis=0)

[purify(x,10) for x in os.listdir()]


def concat2():pass


def biyong(a,b):pass
a=pd.read_excel("1524a.xlsx",na_filter=False)
b=pd.read_excel("1524b.xlsx",na_filter=False)

a=pd.read_excel("2427a.xlsx",na_filter=False)
b=pd.read_excel("2427b.xlsx",na_filter=False)

[z.drop("Unnamed: 0",axis=1,inplace=True) for z in [a,b]]
pd.concat([a,b]).groupby(["project_id","login_id","member_nm"]).sum()
#unconditioanlly merging

ta=pd.merge("","",left_index=True,right_index=True,how="outer")
#index-based 

[x.set_index(["project_id","login_id","member_nm"],inplace=True) for x in [a,b]]

[x.set_index(["id","mail","name"],inplace=True) for x in [da,dbc,ds,na,nbc,ns]]
[x.reset_index(inplace=True) for x in [da,dbc,ds,na,nbc,ns]]

c=pd.concat([da,dbc,ds,na,nbc,ns],axis=0)
c=pd.concat([da,dbc,ds,na,nbc,ns]).drop("nick",axis=1).groupby(["id","mail","name"]).sum()


[x.loc[:,"work":].applymap(lambda w:float(w)) for x in [da,dbc,ds,na,nbc,ns]]

def purify2(fo):
    try:
        u=pd.read_excel(fo,na_filter=False).reset_index()
    except:
        u=pd.read_csv(fo,encoding="utf-8").reset_index()
    u.columns=[
        "date","name","mail","phone","cn","cn0","loc","edu",
        "job","zangae","preg","gzy","bohun","damunwha",
        "choding","daeding",
        "jobtwo","jobno","jobloss","lowincome","jobless",
        "mobuzang","visamarry","bukhan","selfempoly",
        "aihubHx","icHx","consent0","consent1"
    ]
    u.
    u.drop(["consent0","consent1","date","cn0"],axis=1,inplace=True)
    u.drop_duplicates(subset=["name","mail"],inplace=True)
    u.set_index("name",inplace=True)
    u.cn=u.cn.apply(lambda a:"-".join([a[:6],a[6:]]))


    for x in ta.index:
        if len(ta.loc[x,"phone"])==9:
            ta.loc[x,"phone"]="0"+ta.loc[x,"phone"]+"0"
        elif len(ta.loc[x,"phone"])==10:
            ta.loc[x,"phone"]="0"+ta.loc[x,"phone"]
    lambda x:"-".join([x[:3],x[5:9],x[6:10]])
    for x in range(len(c.index)):
        if "crowdworks" in c.index[x][1]:
            c.drop(c.iloc[x],inplace=True)
    

    return u

def purify(fo,danga):
    udf=pd.read_excel(fo,usecols="A:I,K,L,N:P",na_filter=False).drop([0])
    udf.columns=[
        "id","mail","name","nick",
        "work","audit",
        "reaudit","audited","allFinished",
        "dispute","disputeRate",
        "workedTime","workedTimeMean","workedTimeBasis"
        ]
    udf.set_index("id").dropna(axis=0,inplace=True)
    udf.index=udf.index.map(int)
    for t in range(len(udf.index)):
        for s in [udf.workedTime,udf.workedTimeMean]:
            s.iloc[t]=re.findall(r"\((\d+.\d+).\)",s.iloc[t])[0]
    udf.loc[:,"work":]=udf.loc[:,"work":].applymap(lambda r:round(float(r),1))
    udf.loc[:,["work","audit","reaudit","audited","allFinished","dispute"]].applymap(int)
    udf["workedTimePerJob"]=0
    udf["earningPerHour"]=0
    udf["earningPerDay"]=0
    udf["workedTimePerMonth"]=0
    for c in udf.index:
        if udf.loc[c,"workedTime"]>0:
            try:
                udf.loc[c,"workedTimePerJob"]=udf.loc[c,"workedTime"]/(udf.loc[c,"allFinished"]+udf.loc[c,"dispute"])
                udf.loc[c,"earningPerHour"]=(danga*3600)/udf.loc[c,"workedTimePerJob"]
                udf.loc[c,"earningPerDay"]=udf.loc[c,"earningPerHour"]/24
                udf.loc[c,"workedTimePerMonth"]=udf.loc[c,"workedTime"]/31
            except:
                udf.loc[c,"workedTimePerJob"]=0
                udf.loc[c,"earningPerHour"]=0
                udf.loc[c,"earningPerDay"]=0
                udf.loc[c,"workedTimePerMonth"]=0             
        else:
            udf.loc[c,"workedTime"]=0
            udf[c,"workedTimePerJob"]=0
    def uuu(number):
        return round(number,4)
    udf.loc[:,"workedTimePerJob":"workedTimePerMonth"].applymap(uuu)
    return udf

def uu(x):
    if x>0:
        return x/6
    elif x==0:
        return 0
    else:
        return x

al=pd.concat([na,nbc,ns,da,dbc,ds]).groupby(["id","mail","name","nick"]).sum().reset_index()

al.loc[:,"workedTimePerJob":"workedTimePerMonth"].applymap(uu)

        
def auditor():
    return None

ta=pd.read_csv("ta.csv",na_filter=False)

ta.columns=["id","name","mail","nick","phone","auditor"]


(lambda x:"-".join([x[:3],x[5:9],x[6:10]]))


bo.query("(af>9)",inplace=False).query("((af>19)&(audit>29)&(disputeRate<12))|((af>29)&(audit>49)&(disputeRate<17))|((audit>39)&(workedTime>15000)&(disputeRate<8))")

bo0=bo[bo["af"]>10]
bo0=bo0[bo0["work"]>29]
bo0=bo0[bo0["disputeRate"]<15]
bo.query("(af>9)",inplace=False).query("((af>19)&(audit>29)&(disputeRate<12))|((af>29)&(audit>49)&(disputeRate<17))|((audit>39)&(workedTime>15000)&(disputeRate<8))")

bo0.to_excel("boResult.xlsx")

총 작업 수 20개 이하고 올피니시드가 0

test=pd.DataFrame()



pm=pd.read_excel("pmo.xlsx")
ta=pd.read_excel("ta.xlsx")

test=pd.concat([ta,pm],ignore_index=False,axis=0,join="inner",verify_integrity=True)

pm.set_index("name",inplace=True)

pm=pm.applymap(lambda fuck:str(fuck).strip())
ta=ta.applymap(lambda fuck:str(fuck).strip())

test.merge(ta,left_on=["name","citizenNumber","phoneNumber","userLoc","schoolHx","jobCode","zangAe","imSin","gyungDan","boHun","daMunWha","goDing","deDing","twoJob","backSu","muZik","lowIncome","backbackSu","feminist","foreignMarrying","bukHan","selfEmpolyed","aihubHx","cwHx"],right_on=["name","citizenNumber","phoneNumber","userLoc","schoolHx","jobCode","zangAe","imSin","gyungDan","boHun","daMunWha","goDing","deDing","twoJob","backSu","muZik","lowIncome","backbackSu","feminist","foreignMarrying","bukHan","selfEmpolyed","aihubHx","cwHx"])

pm.merge(ta,left_index=True,right_index=True)

pd.concat


ta[~ta.index.duplicated()]

bo,ta=(z.dropna(axis=0,inplace=False).set_index("id") for z in (bo,ta))
ta=ta[["mail","name","nick","phone","auditor"]]
ta.drop(ta.auditor.index[ta.auditor!="O"],inplace=True)
ta.index,bo.index=[z.index.map(int) for z in [ta,bo]]
[z.reset_index() for z in [ta,bo]]
ta=ta.merge(bo,left_on=["id","mail","nick","name"],right_on=["id","mail","nick","name"])


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
    
    for x in bo.loc[z,"work"]:
        if bo.loc[z,"work"]==0:
            for w in CEs.keys():
                CEs[w]=None
                break
        elif bo.loc[z,"work"]<50:

            

	if   bo.loc[z,"work"]==0 or bo.loc[z,"audit"]==0:
		work,audit=0,0
        CEa=0.1
    elif bo.loc[z,"work"]<50:
        work=bo.loc[z,"work"]
        CEa=0.3
	else:
        CEa=bo.loc[z,"worked"]//10+bo.loc[z,"worked"]//1