import os
import math
import re
import pandas as pd

def purify(fo,path="e://auditor"):
    os.chdir(path)
    if ".xls" not in fo:
        try:
            str(fo).replace()


    udf=pd.read_excel(fo,usecols="A:I,K,L,N:P",na_filter=False).drop([0])
    sheetfile=[u for u in os.listdir() if ".xls" in u]
    csvfile=[u for u in os.listdir() if ".csv" in u]
    for u in sheetfile:
        pass
    uname=str(u)
    
    udf.columns=[
        "id","mail","name","nick",
        "work","audit",
        "reaudit","audited","allFinished",
        "dispute","disputeRate",
        "workedTime","workedTimeMean","workedTimeBasis"
        ]
    udf.set_index("id",inplace=True)
    udf.dropna(axis=0,inplace=True)
    udf.index=udf.index.map(int)
    for t in range(len(udf.index)):
        for s in {udf.workedTime,udf.workedTimeMean}:
            s.iloc[t]=re.findall(r"\((\d+.\d+).\)",s.iloc[t])[0]
    udf.loc[:,"work":]=udf.loc[:,"work":].applymap(lambda r:round(float(r),1))
    udf.loc[:,["work","audit","reaudit","audited","allFinished","dispute"]].apply(int)
    return udf
        
def auditor():
    return None

ta=pd.read_csv("ta.csv",na_filter=False)

ta.columns=["id","name","mail","nick","phone","auditor"]





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