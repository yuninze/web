import os,io,json;import pandas as pd;import datetime as dt
ima=str((dt.datetime.now()).strftime("%m%d%H"))
e,enc="utf-8-sig"
os.chdir("D:\\pkr")

def strp(a):
    return str(a).lower().strip()

def pkr(jsonfile,keya,key0,keyb,key1):#extracts email, workerinfo
    if key0 is key1 or keya is keyb:
        raise NameError("keyname")
    elif os.path.isfile(jsonfile)==False:
        raise OSError("nofile")
    elif ".json" not in str(jsonfile):
        raise NameError("ExtensionError")
    else:
        a=json.load(io.open(jsonfile,"r",encoding=enc))
        b=[]
        for x in range(len(a["result"])):
            c=dict()
            c[keya]=strp(a["result"][x][key0]["data"][0]["value"])
            c[keyb]=strp(a["result"][x][key1]["data"][0]["value"])
            b.append(c)
        f=pd.DataFrame(b)
        f=f.set_index("email")
        f.to_csv("pkr_wi_"+ima+".csv",encoding=enc)
        print("...done: object: "+str(len(f.index)))
        return f
#misspelling, non-participated be regarded
#pkr("9730_result_fec8d47d41.json","email","mailaddress","wi","workerinfo")

def pkr_payroll(a,b): #provides payroll target pkr_rawdata: payed cw_email
    if a is b:
        raise NameError("samefile")
    elif all([os.path.isfile(x) for x in [a,b]])==False:
        raise OSError("nofile")
    else:
        a,b=((pd.read_csv(x,encoding=enc)).reset_index(drop=True) for x in [a,b])
        c=a.email.value_counts()
        if len(c[360>c<350])!=0:
            print("...OUTLIER\n"+c.index[360>c<350])
        d=pd.Series((list(set(c[c>=360].index)-set(b.email))),dtype="str",name="unpayeds")
        e=pd.concat([b,d],axis=1)
        if len(d)==0:
            raise OSError("no unpayed")
        e.to_csv("pkr_unpayed_"+ima+".csv",encoding=enc,index=False)
        print("...backlog: "+str(len(d)))
        return e

def pkr_drop(a):#removes 360> from pkr_rawdata
    a=pd.read_csv(a,encoding=enc,usecols=(1,3,5,7,8,9))
    a=a[~a["email"].isin(a["email"].value_counts()[a["email"].value_counts()<360].index)]
    a=a.set_index("email")
    a.to_csv("pkr_dropped_"+ima+".csv",encoding=enc)
#pkr_drop("4df.csv")

def pkr_merg(a,b):#pkr_drop+cw_payeds
    a,b=(pd.read_csv(x,encoding=enc) for x in [a,b])
    a,b=(x.set_index("email") for x in [a,b])
    c=pd.merge(a,b,left_index=True,right_index=True)
    c.to_csv("pikurate_a_"+ima+".csv",encoding=enc)
    return c
pkr_merg("pkr_dropped.csv","pkr_wi_1101.csv")

def pkr_fuk(jf):
    j=json.load(io.open(jf,"r",encoding="utf-8-sig"))
    canvas=[]
    for a in range(len(j["result"])):
        picture=dict()
        picture["wi"]=j["result"][a]["importData_wi"]
        picture["pik_title"]=j["result"][a]["importData_pik_title"]
        picture["category_title"]=j["result"][a]["importData_category_title"]
        picture["memo"]=j["result"][a]["importData_memo"]
        picture["url"]=j["result"][a]["importData_url"]
        picture["ri"]=j["result"][a]["ri"]["data"][0]["value"]
        picture["rating"]=j["result"][a]["rating"]["data"][0]["value"][0]["label"]
        canvas.append(picture)
    b=pd.DataFrame(canvas).sort_values("url")
    b.to_csv(str(jf).replace(".json",".csv"),header=True,index=False,encoding="utf-8-sig") ####
    return b
pkr_fuk("8341_result_ce5140df15.json")

def pkr_rtc(a):
    a=pd.read_csv(a,encoding="utf-8-sig")
    b=(a.raterinfo).values.tolist()
    c=(a.rating).values.tolist()
    return pd.Series(index=['raterinfo0','raterinfo1','raterinfo2'])
    pass

#regex로 str rating 들어간 컬럼 수 세서 6개 이상이고 NaN 아닐 때 row화xx
#중에 reset_index()
#a.loc[:,:].dropna
#a.set_index([((a.reset_index()).index),a.groupby("url").cumcount()])

#os.chdir("C:\\work\\pkr")

def pkr_kkk(a):
    a=pd.read_csv(a)
    a=a.set_index(["url",a.groupby("url").cumcount()]).unstack()
    a.columns=[(f"raterinfo{x}",f"rating{x}") for x in a.columns]
    return a

#(pkr_kkk("pikurate-b-1010.csv")).to_csv("pkrllll.csv",encoding="utf-8-sig")