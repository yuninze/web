import os,json,csv,glob,shutil
import sys
from typing import Counter
import pandas as pd;import datetime as dt;from zipfile import ZipFile
from pathlib import Path
#####################################################################
ima,enc,idea=str((dt.datetime.now()).strftime("%m%d")),"utf-8-sig","=="
sys.setrecursionlimit(1000000)

def strCheck(prop):
    if type(prop) is int or float:
        raise TypeError("a prop should be a str")
    elif type(prop) is str:
        return prop
    else:
        raise TypeError("no such prop")

def EndSwitch(switch):
    while switch:
        for x in ["--","//","\\\\"]:
            print("\b\b"+x,end="")
    return None

def pathStrip(s):
    return str(s).upper().replace("D:\\82\\","")

def garaAO():
    arc=ZipFile("82.zip","r")
    with open("82.zip.csv","w") as csvfile:
        csv.writer(csvfile).writerow(["filename"])
        a=0
        while a<100001:
            for filename in [
                arc.infolist()[x].filename for x in range(
                len(arc.infolist())) if 
                arc.infolist()[x].filename.endswith(".jpg")==True
                ]:
                csv.writer(csvfile).writerow([filename])
                a+=1
    pd.read_csv("82.zip.csv",encoding=enc).to_csv("82.zip.csv",index=False,encoding=enc)

def getjsonfile(path):
    count=0
    for root,dirs,file in os.walk(path):
        for filename in file:
            if filename.endswith(".json"):
                filepath=os.path.join(root,filename)
                pathstring=filepath.replace(path,"e:\\82\\ML")
                os.makedirs(os.path.dirname(pathstring),exist_ok=True)
                shutil.copy(filepath,pathstring)
                count+=1
                print("COPIED: "+filepath+": "+str(count))
    print("DONE: "+str(count)+" files")

def lachk(path="C:/ANNOTATION"):
    os.chdir(path)
    for channeldir in os.listdir():
        os.chdir(channeldir)
        for colordir in os.listdir():
            os.chdir(colordir)
            for seriesdir in os.listdir():
                os.chdir(seriesdir)
                a=glob.glob("*.json")
                for jsonfile in a:
                    if os.stat(jsonfile).st_size==0:
                        os.remove(jsonfile)
                        print("...DELETED: "+jsonfile)
                        continue
                    j=json.load(open(jsonfile,encoding="utf-8"))
                    did=str(j["dataID"])
                    for z in range(len(j["data_set_info"]["data"])):
                        if len(j["data_set_info"]["data"][z]["value"]["metainfo"])!=5:
                            print("METAINFO: "+str(Path(jsonfile).absolute())+":::"+did),input()
                        if j["data_set_info"]["data"][z]["value"]["annotation"]!="POLYGONS":
                            print("POLYGONS: "+str(Path(jsonfile).absolute())+":::"+did),input()
                        if len(j["data_set_info"]["data"][z]["value"]["points"])<1:
                            print("POINTS: "+str(Path(jsonfile).absolute())+":::"+did),input()
                        for objectKeyName in j["data_set_info"]["data"][z]["value"]["object_Label"].keys():
                            if "vehicle" in objectKeyName:
                                if len(j["data_set_info"]["data"][z]["value"]["object_Label"])!=3:
                                    raise IndexError("Unusual/Vehicle/object_Label: "+str(Path(jsonfile).absolute())+":::"+did)
                                elif j["data_set_info"]["data"][z]["value"]["extra"]["value"]!="vehicle":
                                    raise IndexError("Unusual/Vehicle/extra/value: "+str(Path(jsonfile).absolute())+":::"+did)
                                elif j["data_set_info"]["data"][z]["value"]["extra"]["color"]!="#096ecd":
                                    raise IndexError("Unusual/Lane/extra/color: "+str(Path(jsonfile).absolute())+":::"+did)
                            elif "lane" in objectKeyName:
                                if len(j["data_set_info"]["data"][z]["value"]["object_Label"])!=2:
                                    raise IndexError("Unusual Content/Lane: "+str(Path(jsonfile).absolute())+":::"+did)
                                elif j["data_set_info"]["data"][z]["value"]["extra"]["value"]!="lane":
                                    raise IndexError("Unusual/Lane/extra/value: "+str(Path(jsonfile).absolute())+":::"+did)
                                elif j["data_set_info"]["data"][z]["value"]["extra"]["color"]=="#096ecd":
                                    raise IndexError("Unusual/Lane/extra/color: "+str(Path(jsonfile).absolute())+":::"+did)
                        if len(j["data_set_info"]["data"][z]["value"]["object_Label"])==2:
                            if j["data_set_info"]["data"][z]["value"]["object_Label"]["lane_attribute"]=="":
                                print("lane_ERROR: "+str(Path(jsonfile).absolute())+":::"+did)
                                j["data_set_info"]["data"][z]["value"]["object_Label"]["lane_type"]="lane_shoulder"
                                j["data_set_info"]["data"][z]["value"]["object_Label"]["lane_attribute"]="single_solid"
                                print("written")
                        elif len(j["data_set_info"]["data"][z]["value"]["object_Label"])==3:
                            if j["data_set_info"]["data"][z]["value"]["object_Label"]["vehicle_type"]=="":
                                print("vehicle_ERROR: "+str(Path(jsonfile).absolute())+":::"+did)
                                j["data_set_info"]["data"][z]["value"]["object_Label"]["vehicle_type"]="vehicle_bus"
                                j["data_set_info"]["data"][z]["value"]["object_Label"]["vehicle_attribute"]="violation"
                                j["data_set_info"]["data"][z]["value"]["object_Label"]["vehicle_shown"]="hidden"
                                print("written")
                        print("OK: "+str(Path(jsonfile).absolute())+":::"+did)
                    json.dump(j,open(jsonfile,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
                os.chdir("..")
            os.chdir("..")
        os.chdir("..")
    return None

def arcList(fo):
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
    return file,fileBad
    
def arcListInDir(p=os.getcwd()):
    os.chdir("src")
    fileInArc=[]
    fileInArcBad=[]
    arcname=[]
    for detect in os.listdir():
        os.chdir(detect)
        for detectAndNormal in os.listdir():
            os.chdir(detectAndNormal)
            for arcfile in tuple(z for z in os.listdir() 
            if ".zip" in z and ".csv" not in z):
                fileInArc[len(fileInArc):]=arcList(arcfile)[0]
                fileInArcBad[len(fileInArcBad):]=arcList(arcfile)[1]
                arcname[len(arcname):]=[os.path.realpath(arcfile)]
            os.chdir("..")
        os.chdir("..")
    print(idea*5)
    print(arcname)
    print("...current workplace: "+os.getcwd()+os.linesep+idea*5)
    return fileInArc,arcname

def srcKeyname(jsonfile,word):
    try:
        jsonfile=json.load(open(jsonfile,"r",encoding="utf-8-sig"))
    except:
        pass
    try:
        word=str(word)
    except:
        word=int(word)
    pid=jsonfile["projectID"]
    for x in range(len(jsonfile["result"])):
        if jsonfile["result"][x]["unableToWork"]==0:
            for key in jsonfile["result"][x]["falsibi"]:
                    if key.startswith(word):
                        return key,str(pid)

def fal(jsonfile,p="E:\\82\\"):
    if len(jsonfile)!=17:
        raise NameError("jsonfile should contain extractTime")
    else:
        extractTime=str(jsonfile[6:12])
    os.chdir(p)
    try:
        jsonfile=json.load(open(jsonfile,"r",encoding="utf-8-sig"))
    except (OSError):
        print("..proceeding: jsonfile parsed already")
    ng0,ok0,ng1,ok1=0,0,0,0
    e,g={"typeA":[],"typeB":[],"typeC":[],"typeD":[]},[]
    k={"typeA":None,"typeB":None,"typeC":None,"typeD":None}
    try:
        j=jsonfile["result"]
    except:
        if os.path.exists(jsonfile)==False:
            raise OSError("jsonfile does not exist")
        else:
            raise Exception("jsonfile is unusual")
    f,pid=srcKeyname(jsonfile,"importData_file")
    if   pid=="11049":targetPid,rch="11203","normalA" #NA_normalA
    elif pid=="11114":targetPid,rch="11206","normalBC" #NBC_normalBC
    elif pid=="11115":targetPid,rch="11207","normalS" #NS_normalS
    elif pid=="11116":targetPid,rch="11316","detectA" #DA_detectA
    elif pid=="11117":targetPid,rch="11317","detectBC" #DBC_detectBC
    elif pid=="11118":targetPid,rch="11318","detectS" #DS_detectS
    else:
        raise NameError("Pid and RCH does not match")
    for z in range(len(j)):
        if j[z]["unableToWork"]==1:
            ng0+=1
        elif j[z]["unableToWork"]==0:
            ng1+=1
            try:
                ok0+=1
                if j[z][rch]["data"][0]["value"][0]["value"]=="typeA":
                    e["typeA"][len(e["typeA"]):]=[j[z][f]]
                elif j[z][rch]["data"][0]["value"][0]["value"]=="typeB":
                    e["typeB"][len(e["typeB"]):]=[j[z][f]]
                elif j[z][rch]["data"][0]["value"][0]["value"]=="typeC":
                    e["typeC"][len(e["typeC"]):]=[j[z][f]]
                elif j[z][rch]["data"][0]["value"][0]["value"]=="typeD":
                    e["typeD"][len(e["typeD"]):]=[j[z][f]]
            except:
                ke=j[z]["dataID"]
                raise KeyError("Nearby "+str(ng1)+"th object: "+str(ke)+ ": unusual key")
    print("....Parsed")
    arcname=arcListInDir()[1]
    for z in e.keys():
        g+=e[z]
        k[z]=len(e[z])
    for z in e.keys():
        if len(e[z])==0:
            pass
        elif len(e[z])>0:
            for x in arcname:
                print("..at "+str(x))
                arcDirPath=os.path.dirname(x)
                arc=ZipFile(x,"r")
                ab=list(arc.infolist()[x].filename for x in range(len(arc.infolist())) 
                if ".jpg" in arc.infolist()[x].filename)
                for y in e[z]:
                    print("..seeking for "+str(y))
                    if y in ab:
                        nv="569_"+targetPid+"_"+pid+"_"+rch+"_"+str(z)+"_"+str(k[z])+"_"+extractTime
                        foFromArc=arc.extract(member=y)
                        foForEach=foFromArc.replace(p+"src\\",(arcDirPath.replace("\\src\\","\\cat\\"+nv+"\\"))+"\\")
                        try:
                            os.makedirs(os.path.dirname(foForEach),exist_ok=True)
                        except:
                            pass
                        finally:
                            try:
                                os.rename(foFromArc,foForEach)
                            except:
                                pass
                            finally:
                                shutil.rmtree("IMAGE")
                                ok1+=1
                                print("..found: "+str(y)+" > "+str(x)+" "+idea+" count: "+str(ok1))
                    else:
                        continue
    #rchdir=p+"\\cat\\"+rch+"_"+str(z)
    os.chdir(p+"\\cat\\")
    for typedir in os.listdir():
        arcname=str(typedir)
        print("...archiving: "+arcname+".zip")
        shutil.make_archive(arcname,"zip",root_dir=typedir+"\\")
        listfile(arcname+".zip",p=os.getcwd())
    [shutil.rmtree(z,ignore_errors=False) for z in os.listdir() if os.path.isdir(z)==True]
    print(idea*5)
    print("good: "+str(ok0)+":::"+str(ok1)+"  "+"byrd: "+str(ng0))
    [print(str(z)+": "+str(k[z])) for z in e.keys()]
    print(idea*5)
    return None
#fal("11116_122014.json")

def coco(path="e:\\82\\ANNO"):
    os.chdir(path)
    resultSrcfile=[str(os.listdir()[x]).replace(".json",".jpg") for x in 
    range(len(os.listdir())) if ".json" in os.listdir()[x]]
    os.chdir("e:\\82\\src")
    countArc,founds=0,0
    for chasuDir in os.listdir():
        os.chdir(chasuDir)
        for dateDir in os.listdir():
            os.chdir(dateDir)
            arcs=[z for z in os.listdir() if z.endswith(".zip")]
            for targetArc in arcs:
                try:
                    arc=ZipFile(targetArc,"r")
                except:
                    raise OSError("..unexpected file in the last depth")
                jpgInArc=[
                arc.infolist()[x].filename for x in
                range(
                len(arc.infolist())) if 
                arc.infolist()[x].filename.endswith(".jpg") and 
                arc.infolist()[x].file_size!=0
                ]
                for z in resultSrcfile:
                    for y in jpgInArc:
                        if y.endswith(z):
                            arc.extract(y,path="e:\\82\\coco\\")
                            print("..found: "+str(z)+" >> "+str(arc.filename))
                            founds+=1
                        else:
                            continue
            os.chdir("..")
        os.chdir("..")
    return print(str(founds))
#coco()

def undone(srckey,path="e:/82"):
    os.chdir(path)
    doneSrcfilename=[]
    okCount,ngCount,utwCount=0,0,0
    a=[os.listdir()[x] for x in range(len(os.listdir())) if ".json" in os.listdir()[x]]
    if len(a)==0:
        raise OSError("None of jsonfile in the specified path.")
    for z in a:
        j=json.load(open(z,"r",encoding=enc))
        srcKey=srcKeyname(j,srckey)[0]
        for y in range(len(j["result"])):
            if j["result"][y]["unableToWork"]==0:
                try:
                    n=str(j["result"][y]["falsibi"][srcKey])
                    doneSrcfilename[len(doneSrcfilename):]=[n[n.find("IMAGE/"):]]
                    okCount+=1
                except:
                    if len(j["result"][y])<=2:
                        ngCount+=1
                    else:
                        raise Exception("PARSING FAILIURE: "+z+": "+
                        str(j["result"][y]["dataID"]))
            elif j["result"][y]["unableToWork"]==1:
                utwCount+=1
    print("DONE, CNT: "+str(okCount)+", "+str(ngCount)+", "+str(utwCount))
    return doneSrcfilename,okCount,ngCount

def undoing(srckey,jsonfilepath,arcfilepath):
    doneSrcfilename=undone(srckey,path=jsonfilepath)[0]
    print("doneSrcfilename has been loaded.")
    arcNamelistBad=[]
    for x in ["E:/82/0/569_11408_0_72465.zip","E:/82/0/569_11408_1_75922.zip"]:
        arcBad=ZipFile(x,"r")
        arcNamelistBad[len(arcNamelistBad):]=[arcBad.infolist()[x].filename for x in 
        range(len(arcBad.infolist())) 
        if arcBad.infolist()[x].filename.endswith(".jpg")==True 
        and arcBad.infolist()[x].file_size!=0]
    arcBad.close()
    arcNamelist,arcPathString=dict(),dict()
    for r,d,f in os.walk(arcfilepath):
        for filename in f:
            if filename.endswith(".zip"):
                arcFilePathString=os.path.join(r,filename)
                arc=ZipFile(arcFilePathString,"r")
                undoneSrcfilename=[arc.infolist()[x].filename for x in range(len(arc.infolist())) 
                    if arc.infolist()[x].filename.endswith(".jpg")==True 
                    and arc.infolist()[x].file_size!=0]
                next=(set(undoneSrcfilename)-set(doneSrcfilename))-set(arcNamelistBad)
                if len(next)==0:
                    print("DISREGARDING: "+str(arc.filename))
                    arc.close()
                    continue
                else:
                    arcNamelist[arcFilePathString]=list(next)
                print("arcNamelist for "+
                arc.filename+":"+str(len(next))+"/"+str(len(undoneSrcfilename))+
                " has been loaded.")
                arc.close()
    arcNamelistCnt=dict()
    for key in arcNamelist.keys():
        arcNamelistCnt[key]=len(arcNamelist[key])
    arcNamelistCntTotal=sum([x for x in arcNamelistCnt.values()])
    print("arcNamelist total: "+str(arcNamelistCntTotal))
    iterCount=2
    fileCount=0
    extractedCount=0
    for arcName in arcNamelist.keys():
        arc=ZipFile(arcName,"r")
        for file in arcNamelist[arcName]:
            if fileCount>70000:
                newArcname="569_11408_"+str(iterCount)+"_"+str(fileCount)
                print("filecount limit has excceded. ARCHIVING: "+newArcname+".zip")
                os.chdir("E:/82/")
                shutil.make_archive(format="zip",
                root_dir="E:/82/"+str(iterCount),base_name=newArcname,base_dir=str(iterCount)+"/IMAGE")
                iterCount+=1
                fileCount=0
            print("EXTRACTING: "+str(file)+"..."+str(extractedCount)+"/"+str(arcNamelistCntTotal))
            arc.extract(member=file,path="E:/82/"+str(iterCount))
            extractedCount+=1
            fileCount+=1
    print("SUCCESS: "+str(extractedCount)+", "+str(iterCount))
    return None
undoing("sourceValue","C:/Users/yinze/Downloads/82/done","E:/82/target")

def doneSrcfile():
    count=0
    namelisttarget=ZipFile("c:/82.zip","r").namelist()
    namelistjson=[]
    for x in namelisttarget:
        namelistjson[len(namelistjson):]=[x.replace("2021-12-29/ANNOTATION/","").replace("json","jpg")]
    os.chdir("E:/82/target")
    for chasudir in os.listdir():
        os.chdir(chasudir)
        for datedir in os.listdir():
            os.chdir(datedir)
            for zipfile in glob.glob("*.zip"):
                arc=ZipFile(zipfile,"r") 
                for namej in namelistjson:
                    for namea in arc.namelist():
                        if namea.endswith(namej):
                            arc.extract(member=namea,path="C:/82")
                            count+=1
                            print("SUCCESS: "+str(namea)+": "+str(count))
            os.chdir("..")
        os.chdir("..")

def claarc(p="e:\\82\\src"):
    doneSrcfile,okCount,ngCount=undone()
    os.chdir("src")
    if len([u for u in os.listdir() if os.path.isdir(u)==True])>1:
        manyDirsInRoot=True
    else:
        manyDirsInRoot=False
    countArc=0
    for chasuDir in os.listdir():
        os.chdir(chasuDir)
        for dateDir in os.listdir():
            os.chdir(dateDir)
            arcs=[z for z in os.listdir() if z.endswith(".zip")]
            for targetArc in arcs:
                tab={"A":[],"BC":[],"SHOULDER":[]}
                try:
                    arc=ZipFile(targetArc,"r")
                except:
                    raise OSError("..unexpected file in the last depth")
                print(idea*5+os.linesep+"..visiting: "+str(dateDir)+": "+str(arc.filename))
                jpgInArc=[arc.infolist()[x].filename for x in
                range(len(arc.infolist())) if arc.infolist()[x].filename.endswith(".jpg")
                 and arc.infolist()[x].file_size!=0]
                jpgInArcBad=[arc.infolist()[x].filename for x in
                range(len(arc.infolist())) if arc.infolist()[x].filename.endswith(".jpg")
                 and arc.infolist()[x].file_size==0]
                if len(jpgInArcBad)!=0:
                    set(map(print,[l for l in jpgInArcBad])),#input("badfile found: "+str(arc.filename))
                tab["SHOULDER"][len(tab["SHOULDER"]):]=[x for x in jpgInArc if "[SHOULDER]" in x]
                for x in jpgInArc:
                    if "A_BLUE" in x:
                        tab["A"][len(tab["A"]):]=[x]
                    elif "A_WHITE" in x:
                        tab["A"][len(tab["A"]):]=[x]
                    elif "A_YELLOW" in x:
                        tab["A"][len(tab["A"]):]=[x]
                    elif "B_BLUE" in x:
                        tab["BC"][len(tab["BC"]):]=[x]
                    elif "B_WHITE" in x:
                        tab["BC"][len(tab["BC"]):]=[x]
                    elif "B_YELLOW" in x:
                        tab["BC"][len(tab["BC"]):]=[x]
                    elif "C_BLUE" in x:
                        tab["BC"][len(tab["BC"]):]=[x]
                    elif "C_WHITE" in x:
                        tab["BC"][len(tab["BC"]):]=[x]
                    elif "C_YELLOW" in x:
                        tab["BC"][len(tab["BC"]):]=[x]
                print(str(okCount)+":::"+str(ngCount))
                k={"A":None,"BC":None,"SHOULDER":None}
                for z in tab.keys():
                    k[z]=len(tab[z])
                tab={
                    "A":list(set(tab["A"])-set(doneSrcfile)),
                    "BC":list(set(tab["BC"])-set(doneSrcfile)),
                    "SHOULDER":list(set(tab["SHOULDER"])-set(doneSrcfile))
                    }
                for o in tab.keys():
                    if len(tab[o])==0:
                        pass
                    elif len(tab[o])>0:
                        namestring=arc.filename+"_"+o+"_"+str(len(tab[o]))
                        pathstring=str(arc.filename+"/").replace(".zip","")
                        dirstring=str(arc.filename).replace(".zip","")
                        for p in tab[o]:
                            print("extracting: "+str(p))
                            arc.extract(p,path=namestring+"//"+dirstring)
                        with open(namestring+".csv","w") as r:
                            csv.writer(r).writerow(["filename"])
                            for p in tab[o]:
                                csv.writer(r).writerow([pathstring+p])
                    pd.read_csv(
                    namestring
                    +
                    ".csv",
                    encoding=enc
                    ).to_csv(
                    namestring
                    +
                    ".csv",
                    encoding=enc,
                    index=False
                    )
                    print("archiving: "+namestring+".zip")
                    shutil.make_archive(format="zip",root_dir=namestring,base_name=namestring)
                    countArc+=1
                jpgInArc,jpgInArcBad,tab=[],[],dict()
            os.chdir("..")
        os.chdir("..")
    print("..done with "+str(countArc)+" archives")
    return None