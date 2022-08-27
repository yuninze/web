import os,json,glob;import pandas as pd;import datetime as dt
ima,enc=str((dt.datetime.now()).strftime("%m%d")),"utf-8-sig"
os.chdir("d:\\atc\\")

def sani(a):
    return int(a)
#atc0=atc[atc.productname.isin(atc.productname.value_counts().index[atc.productname.value_counts()>1])]
#atc0=atc0[atc0.paytime.isin(atc0.paytime.value_counts().index[atc0.paytime.value_counts()>1])]
#atc0=atc0.drop_duplicates(subset="dataID").sort_values("paytime")
#x=x[~x.paytime.isin(x.paytime.value_counts().index[x.paytime.value_counts()=

def atcR(p):
    os.chdir(p)
    atc=pd.read_csv("atc.csv",encoding=enc).drop_duplicates(subset="dataID",inplace=False)
    atc=atc[atc.productname.isin(atc.productname.value_counts().index[atc.productname.value_counts()!=1])]
    atc=atc.set_index("productname")
    for u in atc.index.unique():
        if len(atc.loc[u])==1:
            atc.drop([u],axis=0,inplace=True)
        elif atc.loc[u,"paytime"].iloc[0]!=atc.loc[u,"paytime"].iloc[1]:
            atc.drop([u],axis=0,inplace=True)
        else:
            continue
    atc.sort_index(inplace=False).to_csv("rev.csv",encoding=enc,index=True)
#atcR("d:\\atc")

def atcG():
    os.chdir("D:\\atc")
    atc,rev=(pd.read_csv(z,encoding=enc).set_index("dataID") for z in ("atc.csv","rev.csv"))
    for z in atc.index.unique():
        if z not in rev.index:
            atc.drop(z,axis=0,inplace=True)
        else:
            continue
    atc["objectNumber"]=None
    for z in atc.index.unique():
        if len(atc.loc[z])==15:
            atc.loc[z,"objectNumber"]="1"
        else:
            atc.loc[z,"objectNumber"]=str(len(atc.loc[z]))
    atc.reset_index(inplace=True).drop_duplicates("dataID",inplace=True)
    for z in atc.index.unique():
        if len(atc.loc[z,"productname"])>3:
            continue
        else:
            for x in range(len(atc.loc[z,"productname"])+1):
                atc.drop(atc.loc[z].iloc[x],inplace=True)
    atc.drop_duplicates("productname",inplace=True).sort_values("productname",inplace=True)
    atc.to_csv("rev0.csv",encoding=enc,index=False)
    return None
atcG()

def atcii(a):
    a=pd.read_csv(open(a,"r",encoding=enc))
    os.chdir("..\\img")
    b=glob.glob("*")
    c=[]
    for x in b:
        if x[0:8] not in (str(x) for x in tuple(a.dataID)):
            c[len(c):]=[x]
            try:
                os.mkdir("atci")
            except:
                pass
            os.rename(x,"atci//"+str(x))
        else:
            continue
    print(len(c))
#atcii("rev.csv")

def atci():
    a=pd.read_csv(open("atc.csv","r",encoding="utf-8-sig"))
    os.chdir("D:\\atc\\atc.xlsx.imagefile\\")
    b=glob.glob("*")
    c=[]
    for x in b:
        if x[0:8] not in (str(x) for x in tuple(a.dataID[~a.productquantity==1])):
            c[len(c):]=[x]
            try:
                os.mkdir("atcbad")
            except:
                pass
            os.rename(x,"atcbad//"+str(x))
        else:
            continue
    print(len(c))
#atci()

def atc(a):
    atc=pd.json_normalize(json.load(open(a,"r",encoding=enc)),record_path="result").filter(regex=r"data")
    atc.columns=atc.columns.str.replace(".data","",regex=False)
    atc.drop("imagefile",axis=1,inplace=True)
    atc=(atc.apply(pd.Series.explode)).set_index("dataID")
    for x in atc.columns:
        atc[x]=atc[x].apply(lambda x:x.get("value"))
    atc["paymentmethod"]=atc["paymentmethod"].apply(lambda x:x.get("대분류"))+"_"+atc["paymentmethod"].apply(lambda x:x.get("소분류"))
    atc=atc.reset_index()
    for x in atc.index:
        atc.shopenvironment[x]=atc.shopenvironment[x][0]["value"]
        atc.usersex[x]=atc.usersex[x][0]["value"]
    atc.to_csv((str(a+"_"+str(len(atc.dataID))+"_"+ima).replace(".json","")+".csv"),encoding=enc,index=False)
    print(atc.sample(n=20,random_state=1))
    return None
#atc("486_9277_export_511_9277_result_a760880003.json")

def atco(a):
    a=pd.read_csv(open(a,"r",encoding=enc)).set_index("dataID")
    b=int(dt.datetime.now().strftime("%Y"))
    c=a.columns.get_loc("useryear")
    for x in range(len(a.index)):
        if b-sani(a.iloc[x,c])<30:
            a.iloc[x,c]=20
        elif b-sani(a.iloc[x,c])<40:
            a.iloc[x,c]=30
        elif b-sani(a.iloc[x,c])<50:
            a.iloc[x,c]=40
        elif b-sani(a.iloc[x,c])<60:
            a.iloc[x,c]=50
        elif b-sani(a.iloc[x,c])<70:
            a.iloc[x,c]=60
        elif b-sani(a.iloc[x,c])>=70:
            a.iloc[x,c]=70
        else:
            a.iloc[x,c]="unknown"
    a.to_csv("atc_"+str(len(a.index))+"_obs.csv",encoding=enc,index=True)
    print(a.sample(n=20,random_state=1))
    return None
#atco("atc_11017_org.csv")

def atcs(a):
    if type(a)==str:
        a=pd.read_csv(open(a,"r",encoding=enc))
    elif type(a)==pd.DataFrame or pd.Series:
        a=a
    a.set_index("dataID",inplace=True)
    print(round((a.index.value_counts().value_counts(normalize=True)*100),2))
    print("..goodNumber")
    return None
#atcs("atc_11017_org.csv")