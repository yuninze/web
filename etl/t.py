import os
import pandas as pd
from typing import Iterable
from type import *

def purify(frame:str,danga:int=10)->tuple:
    '''
    Sanitize BO-derived sheetfile.
    '''
    #Purifying setting upon isaudit
    type,earning=chk_status(frame)
    if type:
        basis="complyRate"
        usecols="A,B,C,D,F,I,K"
    else:
        basis="auditRate"
        usecols="A,B,C,D,E,L,N"
    if earning:
        raise NotImplementedError("earning data exist")
    #Column naming
    cols=["id",
        "mail",
        "name",
        "nick",
        "work",
        basis,
        "TWT"]
    #Attempt to load within settings above
    frame=pd.read_excel(frame,
        usecols=usecols,
        na_filter=True).drop([0])
    frame.columns=cols
    #Fill NaN and null, set indexes
    frame=(frame.applymap(removeblank)
                .set_index(keys=['mail','name']))
    #Try to parsing TWT to float
    frame.TWT=frame.TWT.apply(getvalue)
    #flattening
    frame.loc[:,'work':]=frame.loc[:,'work':].applymap(flat)
    #result meanStats
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
    return (frame,basis)

def concoct(path:str,
        zakupDanga:int,
        auditDanga:int)->pd.DataFrame:
    '''
    Result per-directory frame.
    Recognize zakup and audit.
    Index occurance is ignored.
    '''
    #check auditDanga
    if auditDanga>500:
        print(f"'{auditDanga=}' is peculiar")
    #framefileObject collecting with pathstring
    sheetfiles=[path+"/"+z for z in os.listdir(path) if ".xls" in z]
    frames={}
    #confirm whether frame type
    for framename in sheetfiles:
        if chk_status(framename)[0]:
            danga=auditDanga
        else:
            danga=zakupDanga
        #purify upon frame type
        frames[framename]=purify(framename,danga)[0]
    #unconditional concatenate
    return pd.concat([q for q in frames.values()])

def pmo(frames:Iterable,pii:str='c:/')->pd.DataFrame:
    '''
    Result pii-merged, occdiv-divided result.
    Can take iterable of frames.
    '''
    #check whether an argument consists of frames
    if isinstance(frames,(set,list,dict,tuple)):
        #Concatnate if iterable
        frame=pd.concat(frames)
    else:
        #Frame is frames if non-iterable
        frame=frames
    if isinstance(frames,dict):
        #for dicted frames, it's have not been implemented yet
        if len(frames)<1:
            raise NotImplementedError(f"'{type(frames)}' is peculiar")
    #id, nick protection for disregarding sum
    idx=frame.loc[:,['id','nick']]
    frame=frame.drop(columns=['id','nick'])
    #groupbying and index confirmation
    oldidx=frame.index.nunique(dropna=False)
    frame=frame.groupby(by=frame.index.names)[[
        'work',
        'TWT',
        'TE',
        'TE1000',
        'EPS',
        'EPH',
        'JPH']].transform('sum')
    newidx=frame.index.nunique(dropna=False)
    if not oldidx==newidx:
        raise IndexError('groupbying resulted a non-unique index')
    #id restoration
    frame.loc[:,['id','nick']]=idx
    #aggregate index occurance
    frame.loc[:,'occurance']=frame.index.value_counts()
    #occdiv meanStat, drop temp column, drop index duplicates
    frame=(occdiv(frame[~frame.index.duplicated()])
            .drop('occurance',axis=1)
            .applymap(flat))
    #flattening
    frame['id']=frame['id'].astype(int)
    #try to open pii frame
    piiname=pii
    try:
        pii=pd.read_csv(pii)
        print(f"got '{piiname}'")
        #drop previous index column
        return (pii.drop("Unnamed: 0",axis=1)
                #set index by name and mail
                .set_index(keys=['mail','name'])
                #Merge by index
                .merge(frame,left_index=True,right_index=True))
    except (FileNotFoundError,OSError) as e:
        print(f"{e}")
        return frame

def ctt(
    q,
    w,
    rn:list=None,
    cn:list=None):
    if type(q).__name__=="ndarray":
        if not (rn and cn) is None:
            if type(rn).__name__+type(cn).__name__=="listlist":
                return pd.crosstab(
                    q,
                    w,
                    rownames=rn,
                    colnames=cn)
            return f"cn and rn"
        return f"lenmatch"
    return f"main data type"

def agg(data,mapper):
    return (data.agg(mapper))

def pd2np(q,w,a=1):
    assert q.ndim!=w.ndim

    if a==0:
        assert q.shape[1]!=w.shape[1],"unmetColNum"
        try:r=q.vstack(w)
        except:r=pd.concat((q,w),axis=0)

    elif a==1:
        assert q.shape[0]!=w.shape[0],"unmetRowNum"
        try:r=q.hstack(w)
        except:r=pd.concat((q,w),axis=1)

    else:
        raise Exception("badMath")

    assert r.ndim==q.ndim,"unmetNdim"
    assert r.shape==q.shape,"unmetArrShape"

    return r