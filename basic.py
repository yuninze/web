import os,json,csv,glob,shutil
import pandas as pd;import datetime as dt;from zipfile import BadZipFile, ZipFile
import math;from pathlib import Path
ima,enc,idea=str((dt.datetime.now()).strftime("%m%d")),"utf-8-sig","====="

def strCheck(prop):
    if type(prop) is int or float:
        raise TypeError("a prop should be a str")
    elif type(prop) is str:
        return prop
    else:
        raise TypeError("no such prop")

def pathStrip(s):
    return str(s).upper().replace("D:\\82\\","")

def arcList(fo):
    try:
        arcList=ZipFile(fo,"r").infolist()
        print("..proceeding: "+fo)
        file,fileBad=[],[]
        for z in range(len(arcList)):
            if ".jp" in arcList[z].filename:
                if arcList[z].file_size!=0:
                    file[len(file):]=[arcList[z].filename]
                elif arcList[z].file_size==0:
                    fileBad[len(fileBad):]=[arcList[z].filename]
                else:
                    continue
        if len(fileBad)!=0:
            print("...badfile exists: "+fo)
        return file,fileBad
    except:
        return None,print("bad zipfile: "+fo)

def listfile(arc,p="d:\\"):
    os.chdir(p)
    print("providing listfile")
    c=[]
    for x in ZipFile(arc,"r").namelist():
        if ".jpg" in x:
            c[len(c):]=[x]
        else:
            continue
    namestring=str(arc).replace(".zip",".csv")
    csv.writer(open(namestring,"w",newline="",encoding="utf-8-sig")).writerow(["filename"])
    for x in c:
        csv.writer(open(namestring,"a",newline="",encoding="utf-8-sig")).writerow([x])
    pd.read_csv(namestring,encoding="utf-8-sig").to_csv(namestring,encoding="utf-8-sig",index=False)
    return None
listfile("PRJ-3541.zip",p="C:\\Users\\yinze\\Downloads")

def greatPuzzle_ZeungZuck():
    p="D:\\greatPuzzle\\1126_greatpuzzle\\"
    os.chdir(p)
    a=os.listdir()
    b,c,d,e=[],[],[],[]
    for z in a:
        if "bottle" in z:
            os.chdir(p+z)
            b[len(b):]=glob.glob(r"*.jp*")
            os.chdir("../")
        elif "can" in z:
            os.chdir(p+z)
            c[len(c):]=glob.glob(r"*.jp*")
            os.chdir("../")
        elif "paper" in z:
            os.chdir(p+z)
            d[len(d):]=glob.glob(r"*.jp*")
            os.chdir("../")
        elif "pet" in z:
            os.chdir(p+z)
            e[len(e):]=glob.glob(r"*.jp*")
            os.chdir("../")
        else:continue
    #print("전체 이미지파일 수: "+str(len(b)+len(c)+len(d)+len(e)))
    print("전체 이미지파일 수: "+str(len(set(b+c+d+e))))
    print("유리병 이미지파일 수: "+str(len(b)))
    print("캔/깡통 이미지파일 수: "+str(len(c)))
    print("종이팩 이미지파일 수: "+str(len(d)))
    print("페트병 이미지파일 수: "+str(len(e)))
    return None

def hnx(path,fo):
    os.chdir(path)
    a=pd.read_excel(fo).set_index("성명")
    for z in a.index[a.index.isin(a.index.value_counts().index[a.index.value_counts()>1])]:
        a.loc[z,"금액"]=sum(a.loc[z,"금액"])
    a.drop_duplicates(subset="성명",inplace=True) #
    a["급여"]=a.groupby(["성명","생년월일","성별"])["급여"].transform("sum") #
    return None

def cnnJ(path):
    os.chdir(path)
    fo=glob.glob("*.json")
    canvas=[]
    for a in fo:
        with open(a,"r",encoding=enc) as a:
            canvas[len(canvas):]=[json.load(a)]
    with open("merged.json","w",encoding=enc) as a:
        json.dump(canvas,a)
    return None

def objT(prop):
    os.chdir("")
    j=json.load(open("","r",encoding=enc))
    for z in range(len(j["result"])):
        fileNam=str(j["result"][z][prop]["sourceValue"])
        fileBin=list()
        #[ojb]
        crd=tuple(y for y in j["result"][z][prop]["multipleComponents"])
        obj=j["result"][z][prop]["cat"]
        str(j["result"][z][prop]["data"][0]["value"]["coords"]["tl"])
        with open(str(fileNam),"w") as file:
            file.write(str(objCat)+str(coord).replace("","",1))
        print(str(fileNam)+": "+str(len(objCat)))
        pass
    return None

def cr(p):
    os.chdir(p)
    for a in glob.glob("*"):
        os.chdir(a)
        for b in glob.glob("*"):
            os.chdir(b)
            c=glob.glob("*")
            for x in range(len(c)):
                os.rename(c[x],c[x][c[x].find("_"):].replace("_",str(x+1)+"_",1))
            os.chdir("../")
        os.chdir("../")
    return None

def dcs(path):
    os.chdir(path)
    fs=[]
    fn=[]
    for a in glob.glob("*"):
        os.chdir(a)
        for b in glob.glob("*"):
            os.chdir(b)
            m=glob.glob("*.jpg")
            fn[len(fn):]=[len(m)]
            for c in m:
                fs[len(fs):]=[round(os.path.getsize(c),10)]
            os.chdir("../")
        os.chdir("../")
    print("designComma jpgfileSu: "+str(sum(fn)))
    print("designComma jpgYongRyang: "+str(round(sum(fs)/1024/1024,5))+"MB")
    return None

def cgsItObjNumber(fo):
    os.chdir("C:\\Users\\yinze\\Downloads\\씨지에스아이티_결과데이터_1+2")
    j=json.load(open(fo,"r",encoding=enc))
    zakup=len(j)
    objinJson=[]
    for x in range(zakup):
        objinZakup=len(j[x]["shapes"])
        objinJson[len(objinJson):]=[objinZakup]
    print("zeonche DoneObj(name: label): "+str(sum(objinJson)))
    return None

def hurayPositive(fo):
    os.chdir("C:\\Users\\yinze\\Downloads\\휴레이포지티브_가공2_결과데이터_PMS")
    l=[]
    for z in glob.glob("*"):
        huray=json.load(open(z,"r",encoding=enc))
        print(str(z)+" 데이터 껀수:"+str(len(huray["annotations"])))
        l[len(l):]=[len(huray["annotations"])]
    print("전체 데이터 껀수: "+str(sum(l)))
    return None

def objN0(fo,prop):
    j=json.load(open(fo,"r",encoding=enc))
    try:
        len(j["result"][0][prop])
    except:
        raise IndexError("no such prop")
    zakup=len(j["result"])
    objinJson=[]
    for x in range(zakup):
        objinZakup=len(j["result"][x][prop]["data"])
        objinJson[len(objinJson):]=[objinZakup]
    print("zeonche DoneObj: "+str(sum(objinJson))+os.linesep+"zeonche SrcObj: "+str(zakup))
    return None

def objN1(path):
    os.chdir(path)
    objinJson=list()
    for x in glob.glob("*.json"):
        j=json.load(open(x,"r",encoding=enc))
        for x in range(len(j["data"])):
            objinZakup=len(j["data"][x])
            objinJson[len(objinJson):]=[objinZakup]
    print(str(sum(objinJson)))
    return None

def aum(p):
    os.chdir(p)
    l=[]
    for x in glob.glob("*.json"):
        aum=json.load(open(x,"r",encoding=enc))
        l[len(l):]=[len(aum["data"])]
    print("aum srcNumber: "+str(sum(l)))

def sAgr(*fo,prop):
    strCheck(prop)
    fon=[str(x).replace(r"*.json","") for x in fo]
    print("...visiting")
    fo=(json.load(open(x,"r",encoding=enc)) for x in fo)
    fol=[]
    for x in fo:
        zakups=len(x["result"])
        for y in range(zakups):
            fod=dict()
            fod[fon[fo.index(x)]]=x["result"][y][prop]["sourceValue"]
            fol[len(fol):]=[fod]
        else:
            continue
    for x in range(len(fon)):
        print("..."+fon[x]+": "+str(len(fol[fon])))
    print("...seperating")
    (os.mkdir(x) for x in fon)
    src=glob.glob(r"*.jp*")
    unch=[]
    for x in src:
        for y in [fol[fon[y]]]:
            if x in [fol[fon]]:
                shutil.copy(x,"\\"+y+"\\"+x)
            else:
                unch[len(unch):]=[x]
                continue
        print("...undone :"+str(len(unch)))
    return unch

def remv(target):
    jsondata=json.load(open(target,"r",encoding="utf-8-sig"))
    doneFile=[]
    for a in range(len(jsondata["result"])):
        picture=dict()
        picture['doneFile']=jsondata["result"][a]["hn_img_out"]["sourceValue"]
        doneFile.append(picture)
    df=pd.DataFrame(doneFile)
    jeonbu=(list(df['doneFile']))
    path="D:\\hunature\\raw\\1007_share\\imagefile\\"
    os.chdir(path)
    for filename in os.listdir():
        if filename not in jeonbu:
            os.remove(filename)
        else:
            continue
    return None

def aihub82(fo,p="D:\\aihub82"):
    os.chdir(p)
    arc,arcFilelist=ZipFile(fo,"r"),[]
    
    jpgfile=[]
    for z in arc.namelist():
        if ".jpg" in z:
            jpgfile[len(jpgfile):]=[z]
    jpgfileNumber=len(jpgfile)

    shoulder=[]
    for z in jpgfile:
        if "[SHOULDER]" in z:
            shoulder[len(shoulder):]=[z]
    listfileNameShoulder=str(fo)+"_SHOULDER_"+str(len(shoulder))+".csv"
    with open(listfileNameShoulder,"w",encoding=enc) as a:
        csv.writer(a).writerow(["filename_shoulder"])
        for x in shoulder:
            csv.writer(a).writerow([x])
    pd.read_csv(listfileNameShoulder,encoding=enc).to_csv(listfileNameShoulder,encoding=enc,index=False)

    channela=[]
    for z in jpgfile:
        if "A_BLUE" in z:
            channela[len(channela):]=[z]
        if "A_WHITE" in z:
            channela[len(channela):]=[z]
        if "A_YELLOW" in z:
            channela[len(channela):]=[z]
    listfileNameA=str(fo)+"_A_"+str(len(channela))+".csv"
    with open(listfileNameA,"w",encoding=enc) as a:
        csv.writer(a).writerow(["filename_a"])
        for z in channela:
                csv.writer(a).writerow([z])
    pd.read_csv(listfileNameA,encoding=enc).to_csv(listfileNameA,encoding=enc,index=False)

    channelbc=[]
    for z in jpgfile:
        if "B_BLUE" in z:
            channelbc[len(channelbc):]=[z]
        if "B_WHITE" in z:
            channelbc[len(channelbc):]=[z]
        if "B_YELLOW" in z:
            channelbc[len(channelbc):]=[z]
        if "C_BLUE" in z:
            channelbc[len(channelbc):]=[z]
        if "C_WHITE" in z:
            channelbc[len(channelbc):]=[z]
        if "C_YELLOW" in z:
            channelbc[len(channelbc):]=[z]
    listfileNameBC=str(fo)+"_BC_"+str(len(channelbc))+".csv"
    with open(listfileNameBC,"w",encoding=enc) as a:
        csv.writer(a).writerow(["filename_bc"])
        for z in channelbc:
                csv.writer(a).writerow([z])
    pd.read_csv(listfileNameBC,encoding=enc).to_csv(listfileNameBC,encoding=enc,index=False)
    return print("..done: jpgfileNumber: "+str(jpgfileNumber))
#aihub82(fo="20211129_DETECT_11836.zip",p="E:\\82\\0\\done_piloting\\28차_DETECT_62039\\20211129_DETECT_11836")

#listfileImgSeq("D:\\82")
#aihub82("20211126_DETECT_11571.zip","Z:\\CW_Data\\가공검수필요\\27차_DETECT_58407\\20211126_DETECT_11571\\")
#fal("11118_120716.json","detectS")
#listfile("sample.zip",p="e:\\")
#dcs("D:\\designComma")
#objN1("C:\\save\\aum_result_data_4")
#objN0("livesecu_result_data_3360.json","name_GB9TBX")
#objN1("livesecu_result_data_156841.json")
#objN0("livesecu_result_data_371829.json","name_GB9TBX")