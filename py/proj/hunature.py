import os,json,glob;import pandas as pd;from pandas import json_normalize;import datetime as dt
ima,enc=str((dt.datetime.now()).strftime("%m%d%H")),"utf-8-sig"

def hne():
    os.chdir("d:\\")
    j=json.load(open("hn.json","r",encoding=enc))
    if len(j["result"][0]["importData_HN_AGE"])==1:print("wrong file")
    else:print("processing")
    for z in range(len(j["result"])):
        j["result"][z]["importData_HN_AGE"]=j["result"][z]["importData_HN_AGE"]["data"][0]["value"]
        j["result"][z]["importData_HN_SEX"]=j["result"][z]["importData_HN_SEX"]["data"][0]["value"][0]["value"]
    json.dump(j,open("hne.json","w",encoding=enc),ensure_ascii=False,indent=4)
    return None
hne()

def huNature():
    os.chdir('D:\\huNature')
    j=json.load(open("9260.json","r",encoding=enc))
    c=pd.read_csv("hnException.csv.csv",encoding=enc)
    a=pd.DataFrame()
    os.chdir("..\\img\\hnException")
    hnException=c["filename"].tolist()
    for x in range(len(j["result"])):
        if str(j["result"][x]["sourceValue"]) in ((y[0:8]) for y in hnException):
            a.loc["HN.IMG"][x]=str(j["result"][x]["sourceValue"])
    pass
#

def hng(a):
    an=str(a).replace(".json","")
    a=json_normalize(json.load(open(a,"r",encoding=enc)),record_path=["result"]).filter(regex=r"data")
    a=a.apply(pd.Series.explode)
    a.columns=a.columns.str.replace(".data","",regex=False)
    for b in ["HN_IMG","HN_SEX","HN_AGE"]:
        a[b]=a[b].apply(lambda x:x.get("value"))
    a=a.apply(pd.Series.explode)
    a.HN_IMG=a.HN_IMG.apply(lambda x:x.get('file_name'))
    a.HN_SEX=a.HN_SEX.apply(lambda x:x.get('value'))
    print(a.sample(n=5,random_state=1))
    return a

def hno(a):
    a.HN_SEX=a.HN_SEX.apply(str).replace("FEMALE","3C").replace("MALE","5A")
    a.HN_AGE=a.HN_AGE.apply(int)+2000
    print(a.sample(n=5,random_state=1))
    a.to_csv(str(len(a.index))+".zip.csv",encoding=enc,index=None)
    return None
#hno(hng("9260_result_1b0114c51c.json"))

def hng(a):
    j=json.load(open(a,"r",encoding=enc))
    h=[]
    for d in range(len(j["result"])):
        g=dict()
        g["sourceValue"]=j["result"][d]["hn_img_out"]["sourceValue"]
        g["coords"]=j["result"][d]["hn_img_out"]["data"][0]["value"]["coords"]
        g["hn_sex_e"]=j["result"][d]["hn_img_out"]["data"][0]["value"]["hn_sex_e"][0]["value"]
        g["hn_age_e"]=j["result"][d]["hn_img_out"]["data"][0]["value"]["hn_age_e"][0]["value"]
        g["importData_HN_SEX"]=j["result"][d]["importData_HN_SEX"]
        g["importData_HN_AGE"]=j["result"][d]["importData_HN_AGE"]
        h[len(h):]=[g]
    pd.DataFrame(h).to_csv("hunature.csv",encoding=enc,index=None)
    return None
#hng("hunature.json")

os.chdir('D:\\hunature')
def hni(a):
    a=json.load(open(a,"r",encoding=enc))
    fl=[]
    for x in range(len(a["result"])):
        fl[len(fl):]=[a["result"][x]["hn_img_out"]["sourceValue"]]
    print(".....: "+str(len(fl)))
    print(".....: "+str(len(set(fl))))
    os.chdir("D:\\hunature\\img")
    for x in glob.glob("*"):
        if x not in fl:
            try:
                os.mkdir("hnException")
            except:
                pass
            os.rename(x,"hnException//"+str(x))
        else:
            continue
    return None
#hni("bb.json")