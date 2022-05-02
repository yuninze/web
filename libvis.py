from time import time as t
from typing import Iterable
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

rg=np.random.default_rng(9405)

def hb(q:pd.DataFrame,w):
    t0=t()
    if isinstance(w,Iterable):
        if all(isinstance(q,int) for q in w):
            #a tuple is directly passed to idxer
            #and must be listed
            idxer=list(w)
        else:
            idxer=q.columns.get_indexer(w)
    else:
        idxer=w
    (q.iloc[:50,idxer]
    .plot.barh(figsize=(9,13),title=""))
    plt.show(block=0)
    return f"hb: shown in {t()-t0:.3f}s"

def pc(q:pd.DataFrame,w):
    t0=t()
    #a tuple is directly passed to indexer
    if not q[w].dtype==float:
        (q[w]
        .value_counts(normalize=True)
        .plot.pie(figsize=(9,9),title=""))
        plt.show(block=0)
        return f"pc: shown in {t()-t0:.3f}s"
    #a pie chart is useless for type:
    raise TypeError(f"{q[w].dtype}")

def sp(w,e,title="title",
    a=10,figsize=(12,10)):
    t0=t()
    '''Indicates the innermost relevance'''
    #startup setting
    fg,ax=plt.subplots(figsize=figsize)
    #have area factor by target variable data
    target_var_area=e*a
    while target_var_area.mean()<np.prod(figsize)*.1:
        target_var_area*=.03
    c=rg.random(e.shape[0])
    #plt object
    plt.scatter(x=w,
        y=e,
        s=target_var_area,
        c=c,
        alpha=0.5)
    plt.xlabel(w.name)
    plt.ylabel(e.name)
    plt.title(title)
    plt.show(block=False)
    return f"sp: shown in {t()-t0:.3f}s"

def pp(q,r=None,w=None,e=None,
    kind="scatter",diag_kind="hist",
    hue=None,corner=True):
    '''Indicates sets of the innermost relevance'''
    t0=t()
    #hue is categorical variable
    sns.pairplot(data=q,
        vars=r,
        x_vars=w,y_vars=e,
        kind=kind,diag_kind=diag_kind,
        hue=hue,corner=corner)
    #plt.{x,y}label goes to variable name or its list
    plt.show(block=False)
    return f"pp: shown in {t()-t0:.3f}s"

def hm(q,title="title",figsize=(12,10),
    minmax=(None,None),fmt=".2f",
    corner=""):
    '''Indicates the innermost relevance
    between variables'''
    t0=t()
    #startup setting
    fg,ax=plt.subplots(figsize=figsize)
    #have corr df
    q_corr=q.corr()
    if corner:
        #boolVec to intVec
        mask=np.triu(np.ones_like(q_corr,dtype=bool))
    else:
        mask=None
    cmap=sns.diverging_palette(4,155,as_cmap=True)
    sns.set_theme(style="whitegrid",font="monospace")
    #plt object
    sns.heatmap(q_corr,
        vmin=minmax[0],vmax=minmax[1],
        mask=mask,cmap=cmap,
        annot=True,center=0,square=True,linewidths=.5,fmt=fmt)
    plt.xlabel(f"q.x")
    plt.ylabel(f"q.y")
    plt.title(title)
    plt.show(block=False)
    return f"hm: shown in {t()-t0:.3f}s"

def bp(q,w,e,title="title"):
    '''Cat. vs num. variables: 
    Indicates IQR, median, outliers
    to avoid wrong accept of same median'''
    t0=t()
    fg,ax=plt.subplots(figsize=(12,10))
    #plt object
    sns.boxplot(data=q,
        x=w,
        y=e)
    plt.xlabel(f"{w}")
    plt.ylabel(f"{e}")
    plt.title(f"{title}")
    plt.show(block=False)
    return f"bp: shown in {t()-t0:.3f}s"