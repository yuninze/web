import os,json;import pandas as pd;import operator as op
enc="utf-8-sig"

def strp(s):
        return str(s).strip().replace("\r\n","").replace("\n","")

def tl_cat(a):
    j=json.load(open(a,"r",encoding="utf-8-sig"))
    c=[]
    print("visiting...")
    for y in range(len(j["result"])):
            b=dict()
            b["dataID"]=j["result"][y]["dataID"]
            b["idx"]=j["result"][y]["importData_idx"]
            b["url"]=j["result"][y]["importData_url"]
            b["cat0"]=j["result"][y]["tl_product_cat"]["data"][0]["value"]["대분류"]
            b["cat1"]=j["result"][y]["tl_product_cat"]["data"][0]["value"]["소분류"]
            b["forkid"]=j["result"][y]["tl_product_forKid"]["data"][0]["value"]
            b["foradult"]=j["result"][y]["tl_product_forAdult"]["data"][0]["value"]
            c.append(b)
    c=pd.DataFrame(c)
    for x in range(len(c["idx"])):
        if str(c.iloc[x,5])!="[]":
            c.iloc[x,5]="yes"
        else:
            c.iloc[x,5]="no"
        if str(c.iloc[x,6])!="[]":
            c.iloc[x,6]="yes"
        else:
            c.iloc[x,6]="no"
    for x in range(len(c["dataID"])):
        strp(c.iloc[x,3])
        strp(c.iloc[x,4])
    c.to_csv(str(a).replace(".json","")+"_"+str(len(c.dataID))+".csv",encoding=enc,index=False)
    return None
tl_cat("10183_result_dd8eb9f23f.json")

def tltl(p):
    os.chdir(p)
    target="8361_result_e820a45f1d.json"
    df=pd.json_normalize(json.load(open(target,'r',encoding='utf-8-sig')),record_path='result')
    df=df.drop(list(df.filter(regex='.info')),axis=1,inplace=False).drop(['unableToWork'],axis=1)
    df=df.rename({'importData_filename':'filename'},axis=1).set_index('filename')
    df.columns=df.columns.str.replace('.data','')

    for x in list(df.filter(regex='CHARA')):
        for y in range(len(df.index)):
            df[x][y]=df[x][y][0]['value']

    for x in range(len(df.index)):
        df['CHARATYPE0'][x]=df['CHARATYPE0'][x][0]['value']

        if len(df['CHARATYPE1'][x]) > 1:
            df['CHARATYPE1'][x]=','.join(df['CHARATYPE1'][x])
        if len(df['CHARATYPE1'][x]) == 1:
            df['CHARATYPE1'][x]=df['CHARATYPE1'][x][0]
        if len(df['CHARATYPE1'][x]) == 0:
            df['CHARATYPE1'][x]='NaN'

        df['CHARACOLOR'][x]=','.join([str(a) for a in list(map(op.itemgetter('value'),df['CHARACOLOR'][x]))])
        df['CHARAOUTERLINE'][x]=df['CHARAOUTERLINE'][x][0]['value']
        df['CHARAFACE'][x]=df['CHARAFACE'][x][0]['value']
        df['CHARAPROPOTION'][x]=df['CHARAPROPOTION'][x][0]['value']
        df['CHARABODY'][x]=df['CHARABODY'][x][0]['value']
        #LEG NUMBER-1==CHARA_LEG_INDEX
        #DROP '0' FROM FINAL RESULT COLUMNS
        df['CHARALEG'][x]=df['CHARALEG'][x][0]['value']
        if str(df['CHARALEG'][x])=='없음':
            df['CHARALEG'][x]="다리 없음"
            df['CHARALEGLENGTH0'][x]='NaN'
            df['CHARALEGWEIGHT0'][x]='NaN'
            df['CHARAFOOTSIZE0'][x]='NaN'
        if str(df['CHARALEG'][x])=='1개':
            df['CHARALEGLENGTH0'][x]=df['CHARALEGLENGTH0'][x][0]['value']
            df['CHARALEGWEIGHT0'][x]=df['CHARALEGWEIGHT0'][x][0]['value']
            df['CHARAFOOTSIZE0'][x]=df['CHARAFOOTSIZE0'][x][0]['value']
        if str(df['CHARALEG'][x])=='2개':
            df['CHARALEGLENGTH0'][x]=df['CHARALEGLENGTH1'][x][0]['value']
            df['CHARALEGWEIGHT0'][x]=df['CHARALEGWEIGHT1'][x][0]['value']
            df['CHARAFOOTSIZE0'][x]=df['CHARAFOOTSIZE1'][x][0]['value']
        if str(df['CHARALEG'][x])=='3개':
            df['CHARALEGLENGTH0'][x]=df['CHARALEGLENGTH2'][x][0]['value']
            df['CHARALEGWEIGHT0'][x]=df['CHARALEGWEIGHT2'][x][0]['value']
            df['CHARAFOOTSIZE0'][x]=df['CHARAFOOTSIZE2'][x][0]['value']
        if str(df['CHARALEG'][x])=='4개':
            df['CHARALEGLENGTH0'][x]=df['CHARALEGLENGTH3'][x][0]['value']
            df['CHARALEGWEIGHT0'][x]=df['CHARALEGWEIGHT3'][x][0]['value']
            df['CHARAFOOTSIZE0'][x]=df['CHARAFOOTSIZE3'][x][0]['value']
        if str(df['CHARALEG'][x])=='5개':
            df['CHARALEGLENGTH0'][x]=df['CHARALEGLENGTH4'][x][0]['value']
            df['CHARALEGWEIGHT0'][x]=df['CHARALEGWEIGHT4'][x][0]['value']
            df['CHARAFOOTSIZE0'][x]=df['CHARAFOOTSIZE4'][x][0]['value']
        #ARM NUMBER-1==CHARA_ARM_INDEX
        #DROP '0' FROM FINAL RESULT COLUMNS #5 values
        df['CHARAARM'][x]=df['CHARAARM'][x][0]['value']
        if str(df['CHARAARM'][x])=='팔 없음':
            df['CHARAARMLENGTH0'][x]='NaN'
            df['CHARAARMWEIGHT0'][x]='NaN'
        if str(df['CHARAARM'][x])=='1개':
            df['CHARAARMLENGTH0'][x]=df['CHARAARMLENGTH0'][x][0]['value']
            df['CHARAARMWEIGHT0'][x]=df['CHARAARMWEIGHT0'][x][0]['value']
        if str(df['CHARAARM'][x])=='2개':
            df['CHARAARMLENGTH0'][x]=df['CHARAARMLENGTH1'][x][0]['value']
            df['CHARAARMWEIGHT0'][x]=df['CHARAARMWEIGHT1'][x][0]['value']
        if str(df['CHARAARM'][x])=='3개':
            df['CHARAARMLENGTH0'][x]=df['CHARAARMLENGTH2'][x][0]['value']
            df['CHARAARMWEIGHT0'][x]=df['CHARAARMWEIGHT2'][x][0]['value']
        if str(df['CHARAARM'][x])=='3개 이상':
            df['CHARAARMLENGTH0'][x]=df['CHARAARMLENGTH3'][x][0]['value']
            df['CHARAARMWEIGHT0'][x]=df['CHARAARMWEIGHT3'][x][0]['value']
        #HAND
        df['CHARAHAND'][x]=df['CHARAHAND'][x][0]['value']
        #EYE
        df['CHARAEYE'][x]=df['CHARAEYE'][x][0]['value']
        if str(df['CHARAEYE'][x])=='눈 없음':
            df['CHARAEYESIZE0'][x]='NaN'
            df['CHARAEYEPUPILSIZE0'][x]='NaN'
        if str(df['CHARAEYE'][x])=='눈 1개':
            df['CHARAEYESIZE0'][x]=df['CHARAEYESIZE0'][x][0]['value']
            df['CHARAEYEPUPILSIZE0'][x]=df['CHARAEYEPUPILSIZE0'][x][0]['value']
        if str(df['CHARAEYE'][x])=='눈 2개':
            df['CHARAEYESIZE0'][x]=df['CHARAEYESIZE1'][x][0]['value']
            df['CHARAEYEPUPILSIZE0'][x]=df['CHARAEYEPUPILSIZE1'][x][0]['value']
        if str(df['CHARAEYE'][x])=='눈 3개':
            df['CHARAEYESIZE0'][x]=df['CHARAEYESIZE2'][x][0]['value']
            df['CHARAEYEPUPILSIZE0'][x]=df['CHARAEYEPUPILSIZE2'][x][0]['value']
        if str(df['CHARAEYE'][x])=='눈 3개 이상':
            df['CHARAEYESIZE0'][x]=df['CHARAEYESIZE3'][x][0]['value']
            df['CHARAEYEPUPILSIZE0'][x]=df['CHARAEYEPUPILSIZE3'][x][0]['value']
        #MOUTH
        df['CHARAMOUTH'][x]=df['CHARAMOUTH'][x][0]['value']
        if str(df['CHARAMOUTH'][x])=='입 없음':df['CHARAMOUTHSIZE0'][x]='NaN'
        if str(df['CHARAMOUTH'][x])=='직선형':
            df['CHARAMOUTHSIZE0'][x]=df['CHARAMOUTHSIZE0'][x][0]['value']
        if str(df['CHARAMOUTH'][x])=='곡선형':
            df['CHARAMOUTHSIZE0'][x]=df['CHARAMOUTHSIZE1'][x][0]['value']
        if str(df['CHARAMOUTH'][x])=='꽉 찬 도형':
            df['CHARAMOUTHSIZE0'][x]=df['CHARAMOUTHSIZE2'][x][0]['value']
        if str(df['CHARAMOUTH'][x])=='속 빈 도형':
            df['CHARAMOUTHSIZE0'][x]=df['CHARAMOUTHSIZE3'][x][0]['value']
        if str(df['CHARAMOUTH'][x])=='햄스터형':
            df['CHARAMOUTHSIZE0'][x]=df['CHARAMOUTHSIZE4'][x][0]['value']
        if str(df['CHARAMOUTH'][x])=='인중형':
            df['CHARAMOUTHSIZE0'][x]=df['CHARAMOUTHSIZE5'][x][0]['value']
        if str(df['CHARAMOUTH'][x])=='인간형':
            df['CHARAMOUTHSIZE0'][x]=df['CHARAMOUTHSIZE6'][x][0]['value']
        #TOOTH
        df['CHARATOOTH'][x]=df['CHARATOOTH'][x][0]['value']
        
        #EAR
        df['CHARAEAR'][x]=df['CHARAEAR'][x][0]['value']
        if str(df['CHARAEAR'][x])=='귀 없음':
            df['CHARAEARTYPE0'][x]='NaN'
        if str(df['CHARAEAR'][x])=='얼굴 대비 10~20%':
            df['CHARAEARTYPE0'][x]=df['CHARAEARTYPE0'][x][0]['value']
        if str(df['CHARAEAR'][x])=='얼굴 대비 20~30%':
            df['CHARAEARTYPE0'][x]=df['CHARAEARTYPE1'][x][0]['value']
        if str(df['CHARAEAR'][x])=='얼굴 대비 30~40%':
            df['CHARAEARTYPE0'][x]=df['CHARAEARTYPE2'][x][0]['value']
        if str(df['CHARAEAR'][x])=='얼굴 대비 40~50%':
            df['CHARAEARTYPE0'][x]=df['CHARAEARTYPE3'][x][0]['value']
        if str(df['CHARAEAR'][x])=='얼굴 대비 50% 이상':
            df['CHARAEARTYPE0'][x]=df['CHARAEARTYPE4'][x][0]['value']

        #NOSE
        df['CHARANOSE'][x]=df['CHARANOSE'][x][0]['value']
        if str(df['CHARANOSE'][x])=='코 없음':
            df['CHARANOSESIZE0'][x]='NaN'
        if str(df['CHARANOSE'][x])=='점':
            df['CHARANOSESIZE0'][x]=df['CHARANOSESIZE0'][x][0]['value']
        if str(df['CHARANOSE'][x])=='꽉 찬 콧구멍':
            df['CHARANOSESIZE0'][x]=df['CHARANOSESIZE1'][x][0]['value']
        if str(df['CHARANOSE'][x])=='속 빈 콧구멍':
            df['CHARANOSESIZE0'][x]=df['CHARANOSESIZE2'][x][0]['value']
        if str(df['CHARANOSE'][x])=='직선형':
            df['CHARANOSESIZE0'][x]=df['CHARANOSESIZE3'][x][0]['value']
        if str(df['CHARANOSE'][x])=='곡선형':
            df['CHARANOSESIZE0'][x]=df['CHARANOSESIZE4'][x][0]['value']
        if str(df['CHARANOSE'][x])=='꽉 찬 도형':
            df['CHARANOSESIZE0'][x]=df['CHARANOSESIZE5'][x][0]['value']
        if str(df['CHARANOSE'][x])=='속 빈 도형':
            df['CHARANOSESIZE0'][x]=df['CHARANOSESIZE6'][x][0]['value']
        #APPEREL
        df['CHARAAPPEREL'][x]=df['CHARAAPPEREL'][x][0]['value']

        if len(df['CHARAACC'][x]) > 1:
            df['CHARAACC'][x]=','.join(df['CHARAACC'][x])
        if len(df['CHARAACC'][x]) == 1:
            df['CHARAACC'][x]=df['CHARAACC'][x][0]
        if len(df['CHARAACC'][x]) == 0:
            df['CHARAACC'][x]='NaN'

        df['CHARASIPPO'][x]=df['CHARASIPPO'][x][0]['value']
        df['CHARATAG'][x]=','.join([str(a) for a in list(map(op.itemgetter('value'),df['CHARATAG'][x]))])
    df=df.rename({'CHARATYPE0':'CHARATYPE_a','CHARATYPE1':'CHARATYPE_b'},axis=1)
    (df.drop(list(df.filter(regex=r'[1-9]')),axis=1)).to_csv(target+'.done.csv',encoding='utf-8-sig')
    return None