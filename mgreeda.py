import os,json;import pandas as pd;import datetime as dt
ima,enc=str((dt.datetime.now()).strftime("%Y"+"-"+"%m"+"-"+"%d")),"utf-8-sig"
def mgreeda(p,fo):
    os.chdir(p)
    j=json.load(open(fo,"r",encoding="utf-8-sig"))
    jj=j["result"]
    l=[]
    for x in range(len(jj)):
        d=dict()
        d["dataID"]=jj[x]["dataID"]
        d["신청일"]=str(ima)
        d["이름"]=jj[x]["userName"]["data"][0]["value"]
        d["전번"]=str(jj[x]["userPhone"]["data"][0]["value"]).replace("010","(010)")
        d["연령대"]=jj[x]["userAge"]["data"][0]["value"][0]["value"]
        d["상담시각대"]=jj[x]["availTime"]["data"][0]["value"][0]["value"]
        d["지역"]=jj[x]["userLoc"]["data"][0]["value"][0]["value"]
        d["동의"]="동의함"
        if jj[x]["isVisitClinic"]["data"][0]["value"][0]["value"]=="false":
            d["안과방문주기"]="안과안감"
        else:
            d["안과방문주기"]=jj[x]["visitFreq"]["data"][0]["value"][0]["value"]
        d["3년내수술여부"]=jj[x]["Hx"]["data"][0]["value"]
        d["시력보조도구여부"]=jj[x]["meganeIs"]["data"][0]["value"][0]["value"]
        d["안경렌즈기간"]=jj[x]["meganeHx"]["data"][0]["value"]
        d["노안/백내장의심"]=jj[x]["selfCheck"]["data"][0]["value"][0]["value"]
        #sx=list(j["result"][0]["noanSymptom"]["data"][0]["value"][0]["value"][y] for y in range(len(j["result"][0]["noanSymptom"]["data"][0]["value"])))
        #print(sx)
        #d["증상"]=[os.linesep.join(sx[y] for y in range(len(sx)))]
        l[len(l):]=[d]
    pd.DataFrame(l).to_csv(fo+".csv",encoding=enc,index=False)
    pd.read_csv(fo+".csv",encoding=enc).to_csv(fo+".csv",encoding=enc,index=False)
    return None
mgreeda("E:\\mGreeda","11211_122309.json")