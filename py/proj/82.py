import sys
import os,json,csv,glob,shutil
import pandas as pd
import pathlib
from zipfile import ZipFile

enc='utf-8-sig'
idea='=='

sys.setrecursionlimit(900_000)

def garaAO():
    arc=ZipFile("82.zip","r")
    with open("82.zip.csv","w",encoding='utf-8-sig',newline='') as csvfile:
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
    return None

def getjsonfile(path):
    count=0
    for root,_,file in os.walk(path):
        for filename in file:
            if filename.endswith(".json"):
                filepath=os.path.join(root,filename)
                pathstring=filepath.replace(path,"e:\\82\\ML")
                os.makedirs(os.path.dirname(pathstring),exist_ok=True)
                shutil.copy(filepath,pathstring)
                count+=1
                print("COPIED: "+filepath+": "+str(count))
    print("DONE: "+str(count)+" files")

def lachk(path:str,write:bool=False)->dict:
    '''
    VER. 20220217
    '''
    if not path.endswith('ANNOTATION'):
        raise NameError(f"{path} must end with 'ANNOTATION'")
    car,bus,truck,bike,normal,danger,violation=0,0,0,0,0,0,0
    single_solid,double_solid,single_dashed,left_dashed_double,right_dashed_double=0,0,0,0,0
    lane_white,lane_blue,lane_yellow,lane_shoulder=0,0,0,0
    memo={
        'dataidxs':[],
        'filenames':[],
        'peculiars':[],
        'peculiarspath':[],
        'normal':[],
        'danger':[],
        'violation':[]
    }
    os.chdir(path)
    for channeldir in os.listdir():
        os.chdir(channeldir)
        for colordir in os.listdir():
            os.chdir(colordir)
            for seriesdir in os.listdir():
                os.chdir(seriesdir)
                a=glob.glob(r'*.json')
                for jsonfile in a:
                    if os.stat(jsonfile).st_size==0:
                        os.remove(jsonfile)
                        continue
                    with open(jsonfile,encoding='utf-8',mode='r') as jsondata:
                        filename=pathlib.PurePath(jsonfile)
                        filepath0=os.path.abspath(jsonfile)
                        print(f"attempting: {filename.parts[-1]}")
                        j=json.load(jsondata)
                        dataIdx=str(j['dataID'])
                        memo['dataidxs'].append(int(dataIdx))
                        srcVal=j['data_set_info']['sourceValue']
                        memo['filenames'].append(srcVal)
                        dsi=j["data_set_info"]["data"]
                        #data_id typing
                        if isinstance(j['dataID'],int):
                            j['dataID']=str(j['dataID'])
                        for z in range(len(dsi)):
                            #miVt unconditional substitution
                            miVt=dsi[z]['value']['metainfo']['violation_type']
                            if miVt in (
                                'white',
                                'blue',
                                'shoulder',
                                'yellow'
                            ):
                                dsi[z]['value']['metainfo']['violation_type']=str(miVt).upper()
                                memo['peculiarspath'].append(filepath0)
                            #miTi [0-9]{6}, datetime compatibility
                            miTi=dsi[z]['value']['metainfo']['time_info']
                            if len(miTi)==5:
                                dsi[z]['value']['metainfo']['time_info']=miTi+'0'
                                memo['peculiarspath'].append(filepath0)
                            elif len(miTi)==4:
                                dsi[z]['value']['metainfo']['time_info']=miTi+'00'
                                memo['peculiarspath'].append(filepath0)
                            elif len(miTi)==3:
                                dsi[z]['value']['metainfo']['time_info']=miTi+'000'
                                memo['peculiarspath'].append(filepath0)
                            #miCn [0-9]{3}
                            miCn=dsi[z]['value']['metainfo']['camera_number']
                            if len(miCn)==1:
                                dsi[z]['value']['metainfo']['time_info']=miCn+'00'
                                memo['peculiarspath'].append(filepath0)
                            elif len(miCn)==2:
                                dsi[z]['value']['metainfo']['time_info']=miCn+'0'
                                memo['peculiarspath'].append(filepath0)
                            #pbPoint count
                            if len(dsi[z]['value']['points'])<3:
                                memo['peculiars'].append('_'.join([dataIdx,str(filename),'pbPoint']))
                                memo['peculiarspath'].append(filepath0)
                            if len(dsi[z]["value"]["object_Label"])==3:
                                #check
                                if not dsi[z]["value"]["object_Label"]["vehicle_type"] in (
                                    'vehicle_car',
                                    'vehicle_bus',
                                    'vehicle_truck',
                                    'vehicle_bike'
                                ):
                                    memo['peculiars'].append('_'.join([dataIdx,str(filename),'vehicleType']))
                                    memo['peculiarspath'].append(filepath0)
                                if dsi[z]["value"]["object_Label"]["vehicle_type"]=="vehicle_car":
                                    car+=1
                                elif dsi[z]["value"]["object_Label"]["vehicle_type"]=="vehicle_bus":
                                    bus+=1
                                elif dsi[z]["value"]["object_Label"]["vehicle_type"]=="vehicle_truck":
                                    truck+=1
                                elif dsi[z]["value"]["object_Label"]["vehicle_type"]=="vehicle_bike":
                                    bike+=1
                                #check
                                if not dsi[z]["value"]["object_Label"]["vehicle_attribute"] in (
                                    'normal',
                                    'danger',
                                    'violation'
                                ):
                                    memo['peculiars'].append('_'.join([dataIdx,str(filename),'vehicleAtrb']))
                                    memo['peculiarspath'].append(filepath0)
                                if dsi[z]["value"]["object_Label"]["vehicle_attribute"]=="normal":
                                    normal+=1
                                    memo['normal'].append(int(dataIdx))
                                elif dsi[z]["value"]["object_Label"]["vehicle_attribute"]=="danger":
                                    danger+=1
                                    memo['danger'].append(int(dataIdx))
                                elif dsi[z]["value"]["object_Label"]["vehicle_attribute"]=="violation":
                                    violation+=1
                                    memo['violation'].append(int(dataIdx))
                            elif len(dsi[z]["value"]["object_Label"])==2:
                                #check
                                if not dsi[z]["value"]["object_Label"]["lane_attribute"] in (
                                    'single_solid',
                                    'double_solid',
                                    'single_dashed',
                                    'left_dashed_double',
                                    'right_dashed_double'
                                ):
                                    memo['peculiars'].append('_'.join([dataIdx,str(filename),'laneAtrb']))
                                    memo['peculiarspath'].append(filepath0)
                                if dsi[z]["value"]["object_Label"]["lane_attribute"]=="single_solid":
                                    single_solid+=1
                                elif dsi[z]["value"]["object_Label"]["lane_attribute"]=="double_solid":
                                    double_solid+=1
                                elif dsi[z]["value"]["object_Label"]["lane_attribute"]=="single_dashed":
                                    single_dashed+=1
                                elif dsi[z]["value"]["object_Label"]["lane_attribute"]=="left_dashed_double":
                                    left_dashed_double+=1
                                elif dsi[z]["value"]["object_Label"]["lane_attribute"]=="right_dashed_double":
                                    right_dashed_double+=1
                                #check
                                if not dsi[z]["value"]["object_Label"]["lane_type"] in (
                                    'lane_white',
                                    'lane_blue',
                                    'lane_yellow',
                                    'lane_shoulder'
                                ):
                                    memo['peculiars'].append('_'.join([dataIdx,str(filename),'laneType']))
                                    memo['peculiarspath'].append(filepath0)
                                if dsi[z]["value"]["object_Label"]["lane_type"]=="lane_white":
                                    lane_white+=1
                                elif dsi[z]["value"]["object_Label"]["lane_type"]=="lane_blue":
                                    lane_blue+=1
                                elif dsi[z]["value"]["object_Label"]["lane_type"]=="lane_yellow":
                                    lane_yellow+=1
                                elif dsi[z]["value"]["object_Label"]["lane_type"]=="lane_shoulder":
                                    lane_shoulder+=1
                        if write:
                            json.dump(j,open(jsonfile,mode='w',encoding='utf-8'),ensure_ascii=False,indent=1)
                os.chdir("..")
            os.chdir("..")
        os.chdir("..")
    for q in memo['peculiarspath']:
        filepath1=q.replace('ANNOTATION','ANNOTATIONr')
        filedirpath=os.path.dirname(q).replace('ANNOTATION','ANNOTATIONr')
        os.makedirs(filedirpath,exist_ok=True)
        shutil.copy(src=q,dst=filepath1)
    print(
    f'car: {car}, bus: {bus}, truck: {truck}, bike: {bike}, \n'+
    f'normal: {normal}, danger: {danger}, violation: {violation},\n'+
    f'SS: {single_solid}, SD: {single_dashed}, DS: {double_solid},\n'+
    f'LDD: {left_dashed_double}, RDD: {right_dashed_double},\n'+
    f'LW: {lane_white}, LB: {lane_blue}, LY: {lane_yellow}, LS: {lane_shoulder},\n'
    )
    return memo

def arcList(fo):
    arcList=ZipFile(fo).infolist()
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
        jsonfile=json.load(open(jsonfile,encoding=enc))
    except:
        pass
    word=str(word)
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