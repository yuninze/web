import os,json;import pandas as pd;import datetime as dt
ima=str((dt.datetime.now()).strftime("%Y"+"-"+"%m"+"-"+"%d"))
enc="utf-8-sig"

def CallJson(fileObject):
    try:
        with open(fileObject,"r",encoding=enc) as fileObject:
            return json.load(fileObject)
    except:
        raise OSError("")

def DictToCsv(object,namestring):
    try:
        import pandas as pd
    except:
        pass
    finally:
        pd.DataFrame(object).to_csv(namestring,encoding=enc,index=False)
        pd.read_csv(namestring,encoding=enc).to_csv(namestring,encoding=enc,index=False)
        return None

def jurye(p,fo):
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
        l[len(l):]=[d]
    pd.DataFrame(l).to_csv(fo+".csv",encoding=enc,index=False)
    pd.read_csv(fo+".csv",encoding=enc).to_csv(fo+".csv",encoding=enc,index=False)
    return None

def oppai(path,fileObject):
    os.chdir(path)
    jsondata=CallJson(fileObject)
    jsonpath=jsondata["result"]
    canvas=[]
    for z in range(len(jsonpath)):
        paper=dict()
        paper["전달일"]=ima
        paper["성함"]=jsonpath[z]["username"]["data"][0]["value"]
        userphone=str(jsonpath[z]["userphone"]["data"][0]["value"])
        paper["전번"]="-".join([userphone[:3],userphone[3:7],userphone[7:]])
        paper["연령대"]=jsonpath[z]["useragerange"]["data"][0]["value"][0]["value"]
        paper["지역"]=jsonpath[z]["userloc"]["data"][0]["value"][0]["value"]
        paper["가슴성형고민기간"]=jsonpath[z]["nayamiduration"]["data"][0]["value"][0]["value"]
        nayamitype=jsonpath[z]["nayamitype"]["data"][0]["value"]
        nt=[nayamitype[z]["value"] for z in range(len(nayamitype))]
        paper["가슴성형고민주제"]="\n".join(nt[z] for z in range(len(nt)))
        paper["성형후컵사이즈"]=jsonpath[z]["desiredcup"]["data"][0]["value"][0]["value"]
        paper["원하는수술결과"]=jsonpath[z]["intendedix"]["data"][0]["value"][0]["value"]
        paper["3D가상성형진단원함"]=jsonpath[z]["after3dcomp"]["data"][0]["value"][0]["value"]
        paper["술후무한관리원함"]=jsonpath[z]["infservice"]["data"][0]["value"][0]["value"]
        aftervisitprocess=jsonpath[z]["aftervisitprocess"]["data"][0]["value"]
        avp=[aftervisitprocess[z]["value"] for z in range(len(aftervisitprocess))]
        paper["내원후희망프로세스"]="\n".join(avp[z] for z in range(len(avp)))
        paper["id"]=str(jsonpath[z]["dataID"])
        canvas[len(canvas):]=[paper]
    filenamestring="wonzin_"+ima+"_"+str(len(jsonpath))+".csv"
    DictToCsv(canvas,filenamestring)
    return None
oppai("c:/","Wonzin_2022-01-09_24.json")