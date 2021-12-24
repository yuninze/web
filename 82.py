import os,json,csv,shutil
import sys
import pandas as pd;import datetime as dt;from zipfile import ZipFile
from basic import listfile
ima,enc,idea=str((dt.datetime.now()).strftime("%m%d")),"utf-8-sig","=="
sys.setrecursionlimit(1000000)

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
    arcList=ZipFile(fo,"r").infolist()
    print("..proceeding: "+fo)
    file,fileBad=[],[]
    for z in range(len(arcList)):
        if ".jp" in arcList[z].filename:
            if arcList[z].file_size!=0:
                file[len(file):]=[arcList[z].filename]
            #elif arcList[z].file_size==0:
                #fileBad[len(fileBad):]=[arcList[z].filename]
            else:
                continue
    return file,#fileBad
    
def arcListInDir(p=os.getcwd()):
    os.chdir("src")
    fileInArc=[]
    fileInArcBad=[]
    arcname=[]
    for detect in os.listdir():
        os.chdir(detect)
        for detectAndNormal in os.listdir():
            os.chdir(detectAndNormal)
            for arcfile in tuple(z for z in os.listdir() if ".zip" in z and ".csv" not in z):
                fileInArc[len(fileInArc):]=arcList(arcfile)[0]
                #fileInArcBad[len(fileInArcBad):]=arcList(arcfile)[1]
                arcname[len(arcname):]=[os.path.realpath(arcfile)]
            os.chdir("..")
        os.chdir("..")
    print(idea*5)
    print(arcname)
    print("...current workplace: "+os.getcwd()+os.linesep+idea*5)
    return fileInArc,arcname
#arcListInDir(p="E:\\82\\intact\\done_org")

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
        for key in jsonfile["result"][x]:
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

def coco(pathBase="e:\\82\\ANNO"):
    os.chdir(pathBase)
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
                jpgInArcBad=[
                arc.infolist()[x].filename for x in
                range(
                len(arc.infolist())) if 
                arc.infolist()[x].filename.endswith(".jpg") and 
                arc.infolist()[x].file_size==0
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

def undone(path="e:\\82"):
    os.chdir(path)
    doneSrcfile=[]
    okCount,ngCount=0,0
    for z in [os.listdir()[x] for x in range(len(os.listdir())) if ".json" in os.listdir()[x]]:
        j=json.load(open(z,"r",encoding=enc))
        srcValue,pid=srcKeyname(j,"importData_filename")
        for y in range(len(j["result"])):
            try:
                doneSrcfile[len(doneSrcfile):]=[j["result"][y][srcValue]]
                okCount+=1
            except:
                if len(j["result"][y])<=2:
                    ngCount+=1
                else:
                    raise Exception("..Parsing Failure at Position "+str(j["result"][y]["dataID"]))
    print("....Parsing Done")
    return doneSrcfile,okCount,ngCount

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
                    pd.read_csv(namestring+".csv",encoding=enc).to_csv(namestring+".csv",encoding=enc,index=False)
                    print("archiving: "+namestring+".zip")
                    shutil.make_archive(format="zip",root_dir=namestring,base_name=namestring)
                    countArc+=1
                jpgInArc,jpgInArcBad,tab=[],[],dict()
            os.chdir("..")
        os.chdir("..")
    print("..done with "+str(countArc)+" archives")
    return None
claarc()