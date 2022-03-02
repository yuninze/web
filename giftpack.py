import os,json;import numpy as np;import pandas as pd;import uuid;
p,enc="c:\\","utf-8-sig"
os.chdir(p)
#select_dtypes, 
gp=pd.read_excel("giftpack_true.xlsx").drop("dataID",axis=1,inplace=False)
gp.birthdate[np.isnan(gp.birthdate)==True]=gp.birthdate.mean() #math.isnan()
for z in gp.index:
    gp.birthdate[z]=2021-int(gp.birthdate[z].year)
for y in gp.index:
    try:
        int(gp.birthdate[y])
    except:continue
    finally:
        if gp.birthdate[y]<20:
            gp.birthdate[y]=10
        elif gp.birthdate[y]<30:
            gp.birthdate[y]=20
        elif gp.birthdate[y]<40:
            gp.birthdate[y]=30
        elif gp.birthdate[y]<50:
            gp.birthdate[y]=40
        elif gp.birthdate[y]<60:
            gp.birthdate[y]=50
        elif gp.birthdate[y]<70:
            gp.birthdate[y]=60
        else:
            gp.birthdate[y]=70
gp.sex[gp.sex=="남"],gp.sex[gp.sex=="여"]="male","female"
gp.rename(columns={"birthdate":"age"},inplace=True)
gpBin=round(gp.iloc[:,4:].apply(pd.value_counts,normalize=True),2)
#feature dobCategorize

os.chdir("D:\\giftpack\\raw\\")
def gpToCw():
    target='giftpacksource.csv'
    df=pd.DataFrame(pd.read_csv(target,encoding='utf-8-sig'))
    df=df.drop(df.columns.difference(['id','sku','name','Category','description','url','image_urls']),axis=1)
    dfiu=df['image_urls'].str.split(',',expand=True)
    df=df.drop(columns=['image_urls'])
    dfiu=dfiu.drop(dfiu.iloc[:,8:148],axis=1).rename(columns={0:'image_url0',1:'image_url1',2:'image_url2',3:'image_url3',4:'image_url4',5:'image_url5',6:'image_url6',7:'image_url7'})
    (pd.concat([df,dfiu],axis=1,join='inner')).to_csv(target+'.done.csv',index=None,header=True,encoding='utf-8-sig')
    print(df.sample(n=20,random_state=1))
    return print("----------")
#

def gp(jn):
    j=json.load(open(jn,"r",encoding="utf-8-sig"))
    dl=[]
    for i in range(len(j["result"])):
        d=dict()
        d["dataID"]=j["result"][i]["dataID"]
        d["id"]=j["result"][i]["importData_id"]
        d["sku"]=j["result"][i]["importData_sku"]
        d["name"]=j["result"][i]["importData_name"]
        if len(j["result"][i])<132:
            d["description"]="exception_None_description"
        else:
            d["description"]=str(j["result"][i]["importData_description"]).replace("\r\n","").replace("\n","")
        d["url"]=j["result"][i]["importData_url"]
        d["imageurl0"]=j["result"][i]["importData_image_url0"]
        d["imageurl1"]=j["result"][i]["importData_image_url1"]
        d["imageurl2"]=j["result"][i]["importData_image_url2"]
        d["imageurl3"]=j["result"][i]["importData_image_url3"]
        d["imageurl4"]=j["result"][i]["importData_image_url4"]
        d["imageurl5"]=j["result"][i]["importData_image_url5"]
        d["imageurl6"]=j["result"][i]["importData_image_url6"]
        d["imageurl7"]=j["result"][i]["importData_image_url7"]
        if len(j["result"][i])<132:
            d["productinfo"]="exception_description"
        else:
            a=tuple(str(j["result"][i]["importData_image_url"+str(z)]) for z in range(8))
            a="_".join(a[y] for y in range(len(a)))
            s=str(j["result"][i]["importData_description"]).replace("\r\n","").replace("\n","")
            w=str(j["result"][i]["importData_name"])+"_"+str(j["result"][i]["importData_url"])
            v=str(uuid.uuid5(uuid.NAMESPACE_DNS,str(j["result"][i]["importData_url"])))
            d["productinfo"]=w+s+"_"+v+"_"+a
        d["C001_L001"]=j["result"][i]["C001_L001"]["data"][0]["value"][0]["value"]
        d["C001_L002"]=j["result"][i]["C001_L002"]["data"][0]["value"][0]["value"]
        d["C001_L003"]=j["result"][i]["C001_L003"]["data"][0]["value"][0]["value"]
        d["C001_L004"]=j["result"][i]["C001_L004"]["data"][0]["value"][0]["value"]
        d["C001_L005"]=j["result"][i]["C001_L005"]["data"][0]["value"][0]["value"]
        d["C001_L006"]=j["result"][i]["C001_L006"]["data"][0]["value"][0]["value"]
        d["C001_L007"]=j["result"][i]["C001_L007"]["data"][0]["value"][0]["value"]

        d["C002_L001"]=j["result"][i]["C002_L001"]["data"][0]["value"][0]["value"]
        d["C002_L002"]=j["result"][i]["C002_L002"]["data"][0]["value"][0]["value"]
        d["C002_L003"]=j["result"][i]["C002_L003"]["data"][0]["value"][0]["value"]
        d["C002_L004"]=j["result"][i]["C002_L004"]["data"][0]["value"][0]["value"]
        d["C002_L005"]=j["result"][i]["C002_L005"]["data"][0]["value"][0]["value"]
        d["C002_L006"]=j["result"][i]["C002_L006"]["data"][0]["value"][0]["value"]
        d["C002_L007"]=j["result"][i]["C002_L007"]["data"][0]["value"][0]["value"]

        d["C003_L001"]=j["result"][i]["C003_L001"]["data"][0]["value"][0]["value"]
        d["C003_L002"]=j["result"][i]["C003_L002"]["data"][0]["value"][0]["value"]
        d["C003_L003"]=j["result"][i]["C003_L003"]["data"][0]["value"][0]["value"]
        d["C003_L004"]=j["result"][i]["C003_L003"]["data"][0]["value"][0]["value"]
        d["C003_L005"]=j["result"][i]["C003_L005"]["data"][0]["value"][0]["value"] ##

        d["C004_L001"]=j["result"][i]["C004_L001"]["data"][0]["value"][0]["value"]
        d["C004_L002"]=j["result"][i]["C004_L002"]["data"][0]["value"][0]["value"]
        d["C004_L003"]=j["result"][i]["C004_L003"]["data"][0]["value"][0]["value"]
        d["C004_L004"]=j["result"][i]["C004_L004"]["data"][0]["value"][0]["value"]
        d["C004_L005"]=j["result"][i]["C004_L005"]["data"][0]["value"][0]["value"]
        d["C004_L006"]=j["result"][i]["C004_L006"]["data"][0]["value"][0]["value"]
        d["C004_L007"]=j["result"][i]["C004_L007"]["data"][0]["value"][0]["value"]
        d["C004_L008"]=j["result"][i]["C004_L008"]["data"][0]["value"][0]["value"]
        d["C004_L009"]=j["result"][i]["C004_L009"]["data"][0]["value"][0]["value"]
        d["C004_L010"]=j["result"][i]["C004_L010"]["data"][0]["value"][0]["value"]
        d["C004_L011"]=j["result"][i]["C004_L011"]["data"][0]["value"][0]["value"]
        d["C004_L012"]=j["result"][i]["C004_L012"]["data"][0]["value"][0]["value"]
        d["C004_L013"]=j["result"][i]["C004_L013"]["data"][0]["value"][0]["value"]
        d["C004_L014"]=j["result"][i]["C004_L014"]["data"][0]["value"][0]["value"]

        d["C005_L001"]=j["result"][i]["C005_L001"]["data"][0]["value"][0]["value"]
        d["C005_L002"]=j["result"][i]["C005_L002"]["data"][0]["value"][0]["value"]
        d["C005_L003"]=j["result"][i]["C005_L003"]["data"][0]["value"][0]["value"]
        d["C005_L004"]=j["result"][i]["C005_L004"]["data"][0]["value"][0]["value"]
        d["C005_L005"]=j["result"][i]["C005_L005"]["data"][0]["value"][0]["value"]
        d["C005_L006"]=j["result"][i]["C005_L006"]["data"][0]["value"][0]["value"]
        d["C005_L007"]=j["result"][i]["C005_L007"]["data"][0]["value"][0]["value"]
        d["C005_L008"]=j["result"][i]["C005_L008"]["data"][0]["value"][0]["value"]
        d["C005_L009"]=j["result"][i]["C005_L009"]["data"][0]["value"][0]["value"]
        d["C005_L010"]=j["result"][i]["C005_L010"]["data"][0]["value"][0]["value"]
        d["C005_L011"]=j["result"][i]["C005_L011"]["data"][0]["value"][0]["value"]
        d["C005_L012"]=j["result"][i]["C005_L012"]["data"][0]["value"][0]["value"]
        d["C005_L013"]=j["result"][i]["C005_L013"]["data"][0]["value"][0]["value"]
        d["C005_L014"]=j["result"][i]["C005_L014"]["data"][0]["value"][0]["value"]
        d["C005_L015"]=j["result"][i]["C005_L015"]["data"][0]["value"][0]["value"]
        d["C005_L016"]=j["result"][i]["C005_L016"]["data"][0]["value"][0]["value"]
        d["C005_L017"]=j["result"][i]["C005_L017"]["data"][0]["value"][0]["value"]
        d["C005_L018"]=j["result"][i]["C005_L018"]["data"][0]["value"][0]["value"]
        d["C005_L019"]=j["result"][i]["C005_L019"]["data"][0]["value"][0]["value"]
        d["C005_L020"]=j["result"][i]["C005_L020"]["data"][0]["value"][0]["value"]
        d["C005_L021"]=j["result"][i]["C005_L021"]["data"][0]["value"][0]["value"]
        d["C005_L022"]=j["result"][i]["C005_L022"]["data"][0]["value"][0]["value"]
        d["C005_L023"]=j["result"][i]["C005_L023"]["data"][0]["value"][0]["value"]
        d["C005_L024"]=j["result"][i]["C005_L024"]["data"][0]["value"][0]["value"]
        d["C005_L025"]=j["result"][i]["C005_L025"]["data"][0]["value"][0]["value"]
        d["C005_L026"]=j["result"][i]["C005_L026"]["data"][0]["value"][0]["value"]
        d["C005_L027"]=j["result"][i]["C005_L027"]["data"][0]["value"][0]["value"]
        d["C005_L028"]=j["result"][i]["C005_L028"]["data"][0]["value"][0]["value"]
        d["C005_L029"]=j["result"][i]["C005_L029"]["data"][0]["value"][0]["value"]

        d["C006_L001"]=j["result"][i]["C006_L001"]["data"][0]["value"][0]["value"]
        d["C006_L002"]=j["result"][i]["C006_L002"]["data"][0]["value"][0]["value"]
        d["C006_L003"]=j["result"][i]["C006_L003"]["data"][0]["value"][0]["value"]
        d["C006_L004"]=j["result"][i]["C006_L004"]["data"][0]["value"][0]["value"]

        d["C007_L001"]=j["result"][i]["C007_L001"]["data"][0]["value"][0]["value"]
        d["C007_L002"]=j["result"][i]["C007_L002"]["data"][0]["value"][0]["value"]
        d["C007_L003"]=j["result"][i]["C007_L003"]["data"][0]["value"][0]["value"]
        d["C007_L004"]=j["result"][i]["C007_L004"]["data"][0]["value"][0]["value"]
        d["C007_L005"]=j["result"][i]["C007_L005"]["data"][0]["value"][0]["value"]
        d["C007_L006"]=j["result"][i]["C007_L006"]["data"][0]["value"][0]["value"]
        d["C007_L007"]=j["result"][i]["C007_L007"]["data"][0]["value"][0]["value"]
        d["C007_L008"]=j["result"][i]["C007_L008"]["data"][0]["value"][0]["value"]
        d["C007_L009"]=j["result"][i]["C007_L009"]["data"][0]["value"][0]["value"]
        d["C007_L010"]=j["result"][i]["C007_L010"]["data"][0]["value"][0]["value"]
        d["C007_L011"]=j["result"][i]["C007_L011"]["data"][0]["value"][0]["value"]
        d["C007_L012"]=j["result"][i]["C007_L012"]["data"][0]["value"][0]["value"]
        d["C007_L013"]=j["result"][i]["C007_L013"]["data"][0]["value"][0]["value"]
        d["C007_L014"]=j["result"][i]["C007_L014"]["data"][0]["value"][0]["value"]
        d["C007_L015"]=j["result"][i]["C007_L015"]["data"][0]["value"][0]["value"]
        d["C007_L016"]=j["result"][i]["C007_L016"]["data"][0]["value"][0]["value"]

        d["C008_L001"]=j["result"][i]["C008_L001"]["data"][0]["value"][0]["value"]
        d["C008_L002"]=j["result"][i]["C008_L002"]["data"][0]["value"][0]["value"]
        d["C008_L003"]=j["result"][i]["C008_L003"]["data"][0]["value"][0]["value"]
        d["C008_L004"]=j["result"][i]["C008_L004"]["data"][0]["value"][0]["value"]
        d["C008_L005"]=j["result"][i]["C008_L005"]["data"][0]["value"][0]["value"]
        d["C008_L006"]=j["result"][i]["C008_L006"]["data"][0]["value"][0]["value"]
        d["C008_L007"]=j["result"][i]["C008_L007"]["data"][0]["value"][0]["value"]
        d["C008_L008"]=j["result"][i]["C008_L008"]["data"][0]["value"][0]["value"]
        d["C008_L009"]=j["result"][i]["C008_L009"]["data"][0]["value"][0]["value"]
        d["C008_L010"]=j["result"][i]["C008_L010"]["data"][0]["value"][0]["value"]
        d["C008_L011"]=j["result"][i]["C008_L011"]["data"][0]["value"][0]["value"]
        d["C008_L012"]=j["result"][i]["C008_L012"]["data"][0]["value"][0]["value"]
        d["C008_L013"]=j["result"][i]["C008_L013"]["data"][0]["value"][0]["value"]
        d["C008_L014"]=j["result"][i]["C008_L014"]["data"][0]["value"][0]["value"]
        d["C008_L015"]=j["result"][i]["C008_L015"]["data"][0]["value"][0]["value"]
        d["C008_L016"]=j["result"][i]["C008_L016"]["data"][0]["value"][0]["value"]
        d["C008_L017"]=j["result"][i]["C008_L017"]["data"][0]["value"][0]["value"]
        d["C008_L018"]=j["result"][i]["C008_L018"]["data"][0]["value"][0]["value"]
        d["C008_L019"]=j["result"][i]["C008_L019"]["data"][0]["value"][0]["value"]
        d["C008_L020"]=j["result"][i]["C008_L020"]["data"][0]["value"][0]["value"]
        d["C008_L021"]=j["result"][i]["C008_L021"]["data"][0]["value"][0]["value"]
        d["C008_L022"]=j["result"][i]["C008_L022"]["data"][0]["value"][0]["value"]
        d["C008_L023"]=j["result"][i]["C008_L023"]["data"][0]["value"][0]["value"]
        d["C008_L024"]=j["result"][i]["C008_L024"]["data"][0]["value"][0]["value"]
        d["C008_L025"]=j["result"][i]["C008_L025"]["data"][0]["value"][0]["value"]
        d["C008_L026"]=j["result"][i]["C008_L026"]["data"][0]["value"][0]["value"]
        d["C008_L027"]=j["result"][i]["C008_L027"]["data"][0]["value"][0]["value"]
        d["C008_L028"]=j["result"][i]["C008_L028"]["data"][0]["value"][0]["value"]
        d["C008_L029"]=j["result"][i]["C008_L029"]["data"][0]["value"][0]["value"]
        d["C008_L030"]=j["result"][i]["C008_L030"]["data"][0]["value"][0]["value"]
        d["C008_L031"]=j["result"][i]["C008_L031"]["data"][0]["value"][0]["value"]
        d["C008_L032"]=j["result"][i]["C008_L032"]["data"][0]["value"][0]["value"]
        d["C008_L033"]=j["result"][i]["C008_L033"]["data"][0]["value"][0]["value"]
        d["C008_L034"]=j["result"][i]["C008_L034"]["data"][0]["value"][0]["value"]
        d["C008_L035"]=j["result"][i]["C008_L035"]["data"][0]["value"][0]["value"]
        dl.append(d)
    pd.DataFrame(dl).to_csv(str(jn).replace(".json",".csv"),index=None,encoding="utf-8-sig")
    return None