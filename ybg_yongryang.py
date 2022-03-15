import json,os,uuid;import datetime as dt
ima,enc=str((dt.datetime.now()).strftime("%m%d")),"utf-8-sig"

os.chdir("O:/deprecated/dv_ybg")
def strp(a):pass

ybg=json.load(open("ybg.json","r",encoding=enc))

for y in range(len(ybg)):
    ybg[str(y)]["1"]["phone_number"]="REDACTED"
    ybg[str(y)]["1"]["email"]="REDACTED"
    ybg[str(y)]["1"]["nickname"]="REDACTED"
    a=str(ybg[str(y)]["1"]["_id"])+"-"+str(uuid.uuid1())+str(uuid.uuid4())+"-"+str(uuid.uuid4().hex)+str(uuid.uuid1())
    b=str(uuid.uuid3(uuid.NAMESPACE_DNS,str(ybg[str(y)]["1"]["_id"])))+str(uuid.uuid5(uuid.NAMESPACE_DNS,str(ybg[str(y)]["1"]["_id"])))
    c=str(uuid.uuid5(uuid.NAMESPACE_URL,str(ybg[str(y)]["1"]["phone_number"])))+str(uuid.uuid5(uuid.NAMESPACE_URL,str(ybg[str(y)]["1"]["_id"])))
    ybg[str(y)]["1"]["_id"]=(((a+b+c)*3+((a+c).replace("a","f0a").replace("0","5a09").replace("1","02a01fac").replace("01","a0ccb"))+((c*2).replace("c","-c00a").replace("1","1ccd0"))+a+b)*4).replace("a","bb").replace("b","ac")
    ybg[str(y)]["0"]=(((a+b+c)*3+((a+c).replace("a","f0a").replace("0","5a09").replace("1","02a01fcac").replace("01","a0ccfb"))+((c*2).replace("c","-ac-0f---0a").replace("1","1f-cc-cd0"))+a)*8).replace("b","06a").replace("0","010")
with open("ybg_done.json","w",encoding=enc) as k:
    json.dump(ybg,k,ensure_ascii=False,indent=2)