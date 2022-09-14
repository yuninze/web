import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from time import time as t
from typing import Iterable
from sklearn.preprocessing import normalize
# from sklearn.cluster import KMeans,AgglomerativeClustering

plt.rcParams["font.family"]="monospace"
rg=np.random.default_rng(94056485)

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
    .plot.barh(title=""))
    plt.show(block=0)
    return f"hb: shown in {t()-t0:.3f}s"

def pc(q:pd.DataFrame,w:str):
    t0=t()
    #a tuple is directly passed to indexer
    if not q[w].dtype==float:
        (q[w]
        .value_counts(normalize=True)
        .plot.pie(title=""))
        plt.show(block=0)
        return f"pc: shown in {t()-t0:.3f}s"
    #a pie chart is useless for type:
    raise TypeError(f"{q[w].dtype}")

def sp(w,e,
    a=10,figsize=(12,10),c=None):
    t0=t()
    '''Indicates the innermost relevance'''
    #startup setting
    fg,ax=plt.subplots(figsize=figsize)

    #have area factor by target variable data
    if e.mean()<1:
        a*=10
        small=False
    if e.mean()>100:
        r=normalize(
            np.vstack(
                (w.to_numpy(),e.to_numpy())))
        w=pd.Series(r[0],name=w.name)
        e=pd.Series(r[1],name=e.name)
        small=True
    if small:
        target_var_area=(e+10)*a
    else:
        target_var_area=e*a
    while target_var_area.mean()<np.prod(figsize)*.5:
        target_var_area*=.05

    #colormap
    if c is None:
        c=rg.random(e.shape[0])

    #plt object
    plt.scatter(x=w,
        y=e,
        s=target_var_area,
        c=c,
        alpha=0.7)
    plt.xlabel(w.name)
    plt.ylabel(e.name)
    plt.title(f"{w.name} versus {e.name}")
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

def hm(q,title="heatmap [-1,1]",figsize=(12,12),
    minmax=(-1,1),fmt=".3f",
    corner=False):
    t0=t()
    #have corr df
    q_corr=q.corr()
    if corner:
        #boolVec to intVec
        mask=np.triu(np.ones_like(q_corr,dtype=bool))
    else:
        mask=None
    plt.subplots(figsize=figsize)
    cmap=sns.diverging_palette(240,10,as_cmap=True)
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

def bp(q,w=None,e=None,title="title"):
    '''Cat. vs num. variables: 
    Indicates IQR, median, outliers'''
    t0=t()
    fg,ax=plt.subplots(figsize=(12,8))
    #plt object
    if w and e is None:
        sns.boxplot(x=q)
    else:
        sns.boxplot(data=q,
            x=w,
            y=e)
    plt.xlabel(f"{w}")
    plt.ylabel(f"{e}")
    plt.title(f"{title}")
    plt.show(block=False)
    return f"bp: shown in {t()-t0:.3f}s"

def dngram(q):
    '''draw dendrogram from scipy linkage array'''
    return sch.dendrogram(sch.linkage(q,method="ward"))

# costco0=pd.read_csv("c:/code/costco.csv").iloc[:,2:]
# costco0.index.name="clientidx"
# costco1=pd.DataFrame(
#     normalize(costco0),columns=costco0.columns)

# plt.figure(figsize=(12,12))
# plt.subplot(311)
# gram=dngram(costco1)
# plt.title("sch.linkage dendrogram")

# csc_ac=AgglomerativeClustering(
#     n_clusters=2,affinity="euclidean",linkage="ward"
#     ).fit_predict(costco1)
# plt.subplot(312)
# plt.scatter(costco1.Milk,costco1.Fresh,c=csc_ac)
# plt.title("AC Milk:Fresh")

# csc_km=KMeans(
#     n_clusters=2,random_state=94056485
#     ).fit_predict(costco1)
# plt.subplot(313)
# plt.scatter(costco1.Milk,costco1.Fresh,c=csc_km)
# plt.title("KMeans Milk:Fresh")