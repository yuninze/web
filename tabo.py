import pandas as pd
import os
from libtype import *

def purify(target,danga=10):
    '''
    Sanitize BO-derived sheetfile.
    '''
    #Purifying setting upon isaudit
    if isaudit(target)=="audit":
        basis="complyRate"
        cols=["id","mail","name","nick","work",basis,"TWT"]
        usecols="A,B,C,D,F,I,K"
    elif isaudit(target)=="zakup":
        basis="auditRate"
        cols=["id","mail","name","nick","work",basis,"TWT"]
        usecols="A,B,C,D,E,L,N"
    else:
        raise IndexError("Unusual frame columns")
    #Attempt to load within settings above
    frame=pd.read_excel(target,usecols=usecols,na_filter=True).drop([0])
    frame.columns=cols
    #Fill NaN and null
    frame=frame.applymap(removeblank)
    #Type basisRate
    frame[basis]=frame[basis].apply(float)
    #Set indexes
    frame.set_index(keys=['mail','name'],inplace=True)
    #Try to parsing TWT to float
    frame.TWT=frame.TWT.apply(getvalue)
    #Regards zero work count
    frame.work=frame.work.apply(getflatnum)
    #Result stats
    for i in frame.index:
        if frame.loc[i,"TWT"]>0:
            frame.loc[i,"TE"]=(frame.loc[i,"work"]*danga)
            frame.loc[i,"TE1000"]=(frame.loc[i,"work"]*danga)/1000
            frame.loc[i,"EPS"]=((frame.loc[i,"work"]*danga)/frame.loc[i,"TWT"])
            frame.loc[i,"EPH"]=((frame.loc[i,"work"]*danga)/frame.loc[i,"TWT"])*3600
            if frame.loc[i,"work"]<1:
                frame.loc[i,"work"]=meaning(sum(frame.loc[:,"work"]),len(frame.loc[:,"work"]))
                frame.loc[i,"TWT"]=meaning(sum(frame.loc[:,"TWT"]),len(frame.loc[:,"TWT"]))
                frame.loc[i,"JPH"]=3600/(frame.loc[i,"TWT"]/frame.loc[i,"work"])
            else:
                frame.loc[i,"JPH"]=3600/(frame.loc[i,"TWT"]/frame.loc[i,"work"])
    return [frame,basis]

def concoction(path,auditDanga,zakupDanga):
    '''
    Result per-directory frame. Recognize zakup and audit.
    '''
    #framefileObject collection with pathstring
    sheetfiles=[path+"/"+z for z in os.listdir(path) if ".xls" in z]
    frames={}
    #Confirm whether frame type
    for framename in sheetfiles:
        if isaudit(framename)=="zakup":
            danga=zakupDanga
        elif isaudit(framename)=="audit":
            danga=auditDanga
        #Purify upon frame type
        frames[framename]=purify(framename,danga)[0]
    #Unconditional concatenate
    frame=pd.concat([y for x,y in frames.items()],axis=0,ignore_index=False)
    return frame

def sansibar(frames,pii='c:/'):
    '''
    Result pii-merged, occdiv-divided result. Take iterable of frames.
    '''
    #Check whether an argument consists of frames
    if isinstance(frames,(set,list,dict,tuple))==False:
        raise TypeError("Argument is not an iterable")
    if isinstance(frames,dict):
        if len(frames)<1:
            raise TypeError("Argument is not an iterable")
    #Concatenate before groupbying
    frame=pd.concat(frames)
    frame=frame.groupby(by=frame.index.names)
    #Transform by sum
    frame=frame.transform("sum")
    #Aggregate index occurance
    frame.loc[:,"occurance"]=frame.index.value_counts()
    #Drop index duplicates
    frame=frame[~frame.index.duplicated()]
    #Occdiv meanStat
    frame=occdivstats(frame)
    #Sanitize temp columns
    frame.drop("occurance",axis=1,inplace=True)
    #Try to open pii frame
    try:
        try:
            pii=pd.read_csv(pii).drop("Unnamed: 0",axis=1)
        except:
            pii=pd.read_csv(pii,encoding='utf-8-sig').drop("Unnamed: 0",axis=1)
        finally:
            #Set index by name and mail
            pii.set_index(keys=['mail','name'],inplace=True)
            #Merge by index
            return pii.merge(frame,left_index=True,right_index=True)
    except:
        print(f"'{pii}' does not exist")
        return frame