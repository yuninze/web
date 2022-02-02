import pandas as pd
import os
from libtype import *

def purify(target,danga=10):
    '''
    Sanitize BO-derived sheetfile.
    '''
    #Purifying setting upon isaudit
    if isaudit(target):
        basis="complyRate"
        usecols="A,B,C,D,F,I,K"
    else:
        basis="auditRate"
        usecols="A,B,C,D,E,L,N"
    #Column naming
    cols=[
        "id",
        "mail",
        "name",
        "nick",
        "work",
        basis,
        "TWT"
    ]
    #Attempt to load within settings above
    frame=pd.read_excel(target,usecols=usecols,na_filter=True).drop([0])
    frame.columns=cols
    #Fill NaN and null
    frame=frame.applymap(removeblank)
    #Set indexes
    frame.set_index(keys=['mail','name'],inplace=True)
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

def concoction(path,zakupDanga,auditDanga):
    '''
    Result per-directory frame. Recognize zakup and audit. Index occurance is ignored.
    '''
    #framefileObject collection with pathstring
    sheetfiles=[path+"/"+z for z in os.listdir(path) if ".xls" in z]
    frames={}
    #Confirm whether frame type
    for framename in sheetfiles:
        if isaudit(framename):
            danga=auditDanga
        else:
            danga=zakupDanga
        #Purify upon frame type
        frames[framename]=purify(framename,danga)[0]
    #unconditional concatenate
    frame=pd.concat([x for x in frames.values()],axis=0,ignore_index=False)
    return frame

def sansibar(frames,pii='c:/'):
    '''
    Result pii-merged, occdiv-divided result. Can take iterable of frames.
    '''
    #check whether an argument consists of frames
    if isinstance(frames,(set,list,dict,tuple)):
        #Concatnate if iterable
        frame=pd.concat(frames)
    else:
        #Frame is frames if non-iterable
        frame=frames
    if isinstance(frames,dict):
        #for dicted frames, it's not have been implemented yet
        if len(frames)<1:
            raise NotImplementedError(f"'{type(frames)}' is peculiar")
    if 'auditRate' and 'complyRate' in frame.columns:
        print('There are both basis in columns. It will be incorrect.')
    #id, nick protection for disregarding sum
    idx=frame.loc[:,['id','nick']]
    frame.drop(columns=['id','nick'],inplace=True)
    #groupbying and index confirmation
    oldidx=frame.index.nunique(dropna=False)
    frame=frame.groupby(by=frame.index.names)[[
        'work',
        'TWT',
        'TE',
        'TE1000',
        'EPS',
        'EPH',
        'JPH'
    ]].transform('sum')
    newidx=frame.index.nunique(dropna=False)
    if not oldidx==newidx:
        raise IndexError('groupbying resulted a non-unique index')
    #id restoration
    frame.loc[:,['id','nick']]=idx
    #aggregate index occurance
    frame.loc[:,'occurance']=frame.index.value_counts()
    #drop index duplicates
    frame=frame[~frame.index.duplicated()]
    #occdiv meanStat
    frame=occdiv(frame)
    #sanitize temp columns
    frame.drop('occurance',axis=1,inplace=True)
    #flattening
    frame=frame.applymap(flat)
    frame['id']=np.uint32(frame['id'])
    #try to open pii frame
    try:
        try:
            pii=pd.read_csv(pii)
        except:
            pii=pd.read_csv(pii,encoding='utf-8-sig')
        finally:
            pii.drop("Unnamed: 0",axis=1,inplace=True)
            #Set index by name and mail
            pii.set_index(keys=['mail','name'],inplace=True)
            #Merge by index
            return pii.merge(frame,left_index=True,right_index=True)
    except:
        print(f"pii file '{pii}' does not exist")
        return frame