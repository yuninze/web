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

def listfileImgSeq(p,fo="seqimglistfile.csv"):
    os.chdir(p)
    a=open(p+fo,"w",encoding=enc)
    imagefileLst,imagefileBad=[],[]
    print("..visiting")
    for dir_image in os.listdir():
        os.chdir(dir_image)
        for dir_abcds in os.listdir():
            os.chdir(dir_abcds)
            for dir_bwsys in os.listdir():
                os.chdir(dir_bwsys)
                for dir_dirss in os.listdir():
                    os.chdir(dir_dirss)
                    for imagefile in os.listdir():
                        if os.path.getsize(imagefile)<100:
                            imagefileBad[len(imagefileBad):]=[pathStrip(Path(imagefile).absolute())]
                        else:
                            imagefileLst[len(imagefileLst):]=[pathStrip(Path(imagefile).absolute())]
                    json.dumps(a,)
                    imagefileLst=[]
                    os.chdir("../")
                os.chdir("../")
            os.chdir("../")
        os.chdir("../")
    if len(os.listdir())>2:
        print("..exception: dir_image")
    else:
        pass
    pd.read_csv("d:\\"+fo,encoding=enc).to_csv("d:\\"+fo,encoding=enc,index=False)
    #.applymap(lambda x:str(x).replace("\\\\","/"))
    return print("..imagefileBad: "+str(len(imagefileBad)))