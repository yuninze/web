import pandas as pd;import os;import re
os.chdir("e:\\auditor")

ta=pd.read_csv("ta.csv",na_filter=False)

ta.columns=["id","name","mail","nick","phone","auditor"]


bo=pd.read_excel("da.xls",usecols="A:I,K,L,N:P",na_filter=False).drop([0])
bo.columns=["id","mail","name","nick","work","audit","reaudit","audited","af","dispute","disputeRate","workedTime","workedTimeMean","workedTimeBasis"]
bo.set_index("id",inplace=True)
bo.index=bo.index.map(int)
bo.dropna(axis=0,inplace=True)
for x in range(len(bo.index)):
    for y in (bo.workedTime,bo.workedTimeMean):
        y.iloc[x]=re.findall(r"\((\d+.\d+).\)",y.iloc[x])[0]
bo.loc[:,"work":]=bo.loc[:,"work":].applymap(lambda t:round(float(t),1))
bo.loc[:,"work"]=bo.loc[:,"work"].apply(int)


bo.query("(af>9)",inplace=False).query("((af>19)&(audit>29)&(disputeRate<12))|((af>29)&(audit>49)&(disputeRate<17))|((audit>39)&(workedTime>15000)&(disputeRate<8))")

bo0=bo[bo["af"]>10]
bo0=bo0[bo0["work"]>29]
bo0=bo0[bo0["disputeRate"]<15]
bo.query("(af>9)",inplace=False).query("((af>19)&(audit>29)&(disputeRate<12))|((af>29)&(audit>49)&(disputeRate<17))|((audit>39)&(workedTime>15000)&(disputeRate<8))")

bo0.to_excel("boResult.xlsx")


총 작업 수 20개 이하고 올피니시드가 0




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