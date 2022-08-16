import os
import json
from datetime import datetime 
import pandas as pd

enc="utf-8-sig"

def ima()->str:
    '''Get strings of current time'''
    return datetime.now().strftime("%y%m%d")

def load_json(filename:str):
    try:
        with open(filename,encoding=enc) as jsonfile:
            return json.load(jsonfile)
    except FileNotFoundError as e:
        return print(f"{e}")

def dict_to_csv(obj:dict,filename:str)->None:
    '''Save dataframe as CSV from dict'''
    (pd.DataFrame(obj)
    .to_csv(filename,encoding=enc,index=False))
    (pd.read_csv(filename,encoding=enc)
    .to_csv(filename,encoding=enc,index=False))
    return None

def clin_oppai(path,fileObject):
    '''Project-specific JSON2CSV'''
    os.chdir(path)
    jsondata=load_json(fileObject)
    jsonpath=jsondata["result"]
    canvas=[]
    for z in range(len(jsonpath)):
        paper=dict()
        paper["전달일"]=ima
        paper["성함"]=jsonpath[z]["username"]["data"][0]["value"]
        userphone=str(jsonpath[z]["userphone"]["data"][0]["value"])
        if len(userphone)==11:
            paper["전번"]="-".join([userphone[:3],userphone[3:7],userphone[7:]])
        else:
            print(f"'{userphone}' has peculiar length")
            paper["전번"]=userphone
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
        canvas.append(paper)
    filenamestring="wonzin_"+ima+"_"+str(len(jsonpath))+".csv"
    dict_to_csv(canvas,filenamestring)
    return None

def clin_noan(path,fileObject):
    '''Project-specific JSON2CSV'''
    os.chdir(path)
    jsondata=load_json(fileObject)
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
        useravailtime=jsonpath[z]["useravailtime"]["data"][0]["value"]
        useravailtime=[useravailtime[z]["value"] for z in range(len(useravailtime))]
        paper["상담시각대"]="\n".join(useravailtime[z] for z in range(len(useravailtime)))
        paper["안과주기적방문여부"]=jsonpath[z]["visitclinc"]["data"][0]["value"][0]["value"]
        if jsonpath[z]["visitclinc"]["data"][0]["value"][0]["value"]=="안과안감":
            paper["안과방문주기"]="안과안감"
        else:
            paper["안과방문주기"]=jsonpath[z]["visitclinicfreq"]["data"][0]["value"][0]["value"]
        aftervisitprocess=jsonpath[z]["aftervisitprocess"]["data"][0]["value"]
        avp=[aftervisitprocess[z]["value"] for z in range(len(aftervisitprocess))]
        paper["내원후희망프로세스"]="\n".join(avp[z] for z in range(len(avp)))
        sx0=jsonpath[z]["sx0"]["data"][0]["value"]
        sx0=[sx0[z]["value"] for z in range(len(sx0))]
        paper["증상체크리스트1"]="\n".join(sx0[z] for z in range(len(sx0)))
        sx1=jsonpath[z]["sx1"]["data"][0]["value"]
        sx1=[sx1[z]["value"] for z in range(len(sx1))]
        paper["증상체크리스트2"]="\n".join(sx1[z] for z in range(len(sx1)))
        paper["id"]=str(jsonpath[z]["dataID"])
        canvas.append(paper)
    filenamestring="jurye_"+ima+"_"+str(len(jsonpath))+".csv"
    dict_to_csv(canvas,filenamestring)
    return None

def ta_english(fileObject,path='c:/'):
    '''Project-specific JSON2CSV'''
    os.chdir(path)
    jsondata=load_json(fileObject)
    jsonpath=jsondata["result"]
    canvas=[]
    for z in range(len(jsonpath)):
        paper=dict()
        paper["추출일"]=ima
        paper["data_idx"]=jsonpath[z]["dataID"]
        paper["전번"]=jsonpath[z]["name_RFEMO0"]["data"][0]["value"]
        tests=jsonpath[z]["name_BEU78U"]["data"][0]["value"]
        tests=[tests[z]["value"] for z in range(len(tests))]
        paper['영어시험이름']="\n".join(tests[z] for z in range(len(tests)))
        paper["영어시험성적"]=jsonpath[z]["name_HV6CYI"]["data"][0]["value"]
        paper['증빙제출동의']='녜'
        paper['전번연락동의']='녜'
        canvas.append(paper)
    filenamestring="english_"+ima+"_"+str(len(jsonpath))+".csv"
    dict_to_csv(canvas,filenamestring)
    return None