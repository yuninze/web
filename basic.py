import os,json,csv,glob,shutil
import pandas as pd
import datetime as dt
from zipfile import ZipFile
ima,enc,idea=str((dt.datetime.now()).strftime("%m%d")),"utf-8-sig","=="

def listing(zipfile):
    '''
    Provide namelist dict of jpegfile in zipfile.
    '''
    with open(zipfile) as zipfile:
        zipfile=ZipFile(zipfile)
        filename=zipfile.filename
        infolist=zipfile.infolist()
        print(f'visiting {filename}')
        namelist={}
        for z in range(len(infolist)):
            jpgfilename=infolist[z].filename
            if '.jp' in filename.lower():
                if infolist[z].file_size!=0:
                    namelist['ok']|=[jpgfilename]
                else:
                    namelist['ng']|=[jpgfilename]
        return filename,namelist

def makemt(zipfile):
    '''
    Write csvfile from namelist dict.
    '''
    filename,namelist=listing(zipfile)
    namestring=filename.replace('.zip','.csv')
    with open(namestring,'w',encoding='utf-8-sig',newline='') as listfile:
        c=csv.writer(listfile)
        c.writerow(['filename'])
        [c.writerow([x]) for x in namelist['ok']]
    if len(namelist['ng'])!=0:
        ngcount=len(namelist['ng'])
    else:
        ngcount=0
    print(f'done {namestring}, omitted {ngcount} file')

def greatPuzzle_ZeungZuck():
    '''
    fuck
    '''
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