import time as t
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from regex import E
import seaborn as sns

rg=np.random.default_rng(9405)
xy=pd.DataFrame(rg.gamma(100,size=(1000,10)),columns=[q for q in range(10)])
sns.set_theme("white")

def bp(q,w,e,title="title"):
    fg,ax=plt.subplots(figsize=(12,10))
    #plt object
    sns.boxplot(data=q,
        x=w,
        y=e)
    plt.xlabel(f"{w}")
    plt.ylabel(f"{e}")
    plt.title(f"{title}")
    return f"bp: shown"

def pp(w,e,title="title",a=10,figsize=(12,10)):
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
    plt.xlabel(f"{w.name}")
    plt.ylabel(f"{e.name}")
    plt.title(f"{title}")
    return f"pp: shown"

def hm(q,title="title",figsize=(12,10),minmax=(None,None),fmt=".2f"):
    #startup setting
    fg,ax=plt.subplots(figsize=figsize)
    #have corr df
    q_corr=q.corr()
    mask=np.triu(np.ones_like(q_corr,dtype=bool))
    cmap=sns.diverging_palette(4,155,as_cmap=True)
    sns.set_theme(style="whitegrid",font="monospace")
    plt.xlabel(f"q.x")
    plt.ylabel(f"q.y")
    plt.title(f"{title}")
    sns.heatmap(q_corr,
        vmin=minmax[0],vmax=minmax[1],
        mask=mask,cmap=cmap,
        annot=True,center=0,square=True,linewidths=.5,fmt=fmt)
    return f"hm: shown"

###
def sb(q,w,e,title="title"):
    #innermost EDAs
    sns.pairplot(xy,x_vars=[],y_vars=target_vars,size=4,aspect=1,kind="scatter")
    plt.show(block=0)

#for numeric data
sns.pairplot(xy,hue="f{categorizable/indexable_data_label}",diag_kind="hist")