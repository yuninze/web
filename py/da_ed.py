from glob import glob
import numpy as np
import pandas as pd
import scipy.stats
from full_fred.fred import Fred
from da_vis import *


# innermost params
pd.options.display.min_rows=6
pd.options.display.float_format=lambda q:f"{q:.5f}"


def truthy(*vals):
    for x in vals:
        if not x:
            raise SystemExit(f"{x}")


def full_range_idx(f:pd.DataFrame,
    test=False)->pd.DataFrame:
    if test: # frame with full-range date indices
        return np.arange(
            f.index.min(),f.index.max(),dtype="datetime64[D]")
    return (pd.DataFrame(
        pd.date_range(
            f.index.min(),f.index.max()),columns=["date"])
            .set_index("date"))


def messij(f:pd.DataFrame)->pd.DataFrame:
    return f.apply(pd.to_numeric,errors="coerce")


def getdata(local:bool=True,
    roll:bool=False,roll_n:int=3)->pd.DataFrame:
    t0=t()
    if local:
        f=(pd.read_csv("c:/code/data0.csv",
            index_col="date",
            converters={"date":pd.to_datetime},
            na_filter=False)
            .apply(pd.to_numeric,errors="coerce"))
    else:
        int={
            "cys":"BAMLH0A0HYM2",
            "5yi":"T5YIE",
            "10yt":"DGS10",
            "ng":"DHHNGSP",
            "wti":"DCOILWTICO",
        }
        ext={
            "zs":"soybean",
            "hg":"copper",
        }
        fed=Fred("c:/code/fed")
        fs={i:fed.get_series_df(int[i])
            .loc[:,"date":]
            .astype({"date":"datetime64[ns]"})
            .set_index("date")
            .rename(columns={"value":i}) for i in int}
        fsincsv=[pd.read_csv(q,
            index_col="date",
            converters={"date":pd.to_datetime},
            na_filter=False) for q in sorted(glob(r"c:/code/da_*.csv"))]
        for q in range(len((fsincsv))):
            fs[f"{fsincsv[q].columns[0]}"]=fsincsv[q]
        f=messij(pd.concat(fs.values(),axis=1))
        f.to_csv("c:/code/data0.csv",encoding="utf-8-sig")
    if roll:
        try:
            f=f.rolling(roll_n,min_periods=3).mean()
            print(f"min_periods=3")
        except:
            f=f.rolling(roll_n,min_periods=1).mean()
            print(f"min_periods=1")
    print(f"elapsed {t()-t0:.2f}s (getdata): got")
    return f


def zs(f:pd.DataFrame,pctrng=(0.2,99.8))->pd.DataFrame:
    t0=t()
    fcache=[]
    for i in f.columns:
        print(f"zs::col::{i}")
        q=f[i].dropna()
        mm=np.percentile(q,pctrng)
        q[(q<=mm[0])|(q>=mm[1])]=np.nan
        q=q.dropna()
        nor_zs=scipy.stats.zscore(q)
        log_zs=pd.DataFrame(scipy.stats.zscore(
            scipy.stats.yeojohnson(q)[0]),index=q.index)
        prb_zs=pd.concat(
                [pd.DataFrame(w,index=q.index) for w in 
                [scipy.stats.norm.pdf(np.absolute(e)) for e in 
                [nor_zs,log_zs]]]
                ,axis=1)
        w=(pd.concat([q,nor_zs,log_zs,prb_zs],axis=1)
            .set_axis(
                [f"{i}",f"{i}nzs",f"{i}lzs",f"{i}nzsprb",f"{i}lzsprb"],
                axis=1))
        fcache.append(w)
    f=full_range_idx(f).join(pd.concat(fcache,axis=1),how="left")
    f.to_csv("c:/code/data1.csv",encoding="utf-8-sig",)
    print(f"elapsed {t()-t0:.2f}s (zs): {pctrng}")
    return f


def prbrng(f:pd.DataFrame,i:str,rng=(.05,5),dropna=True,
    test=False)->pd.DataFrame:
    t0=t()
    if not i in f.columns:
        raise NameError(f"{i} not exist in columns")
    colp=f"{i}lzsprb"
    if test:
        rng=np.delete(np.round(np.flip(
                    np.geomspace(rng[0],1,rng[1])
                    ),2),2)
    else:
        rng=np.round(np.flip(np.percentile(
            f[colp].dropna(),(5,10,20,40,100)
            )),2)
    f.loc[:,f"{colp}rng"]=None
    for q in range(len(rng)):
        f.loc[:,f"{colp}rng"]=np.where(
            (~pd.isna(f[colp])) & (f[colp]<=rng[q]),
            rng[q],f[f"{colp}rng"])
    if dropna:
        f=f.dropna(subset=f"{colp}rng")
    f[f"{colp}rng"]=f[f"{colp}rng"].astype("category")
    print(f"elapsed {t()-t0:.2f}s (prng): {rng}")
    return f


def mon(f:pd.DataFrame,start:int,stop:int):
    a=sum([f.index.month==q for q in np.arange(start,stop,1)])
    return np.asarray(a,dtype="bool")


def locate(f,i:str,v:float,test=True):
    rowidx=np.abs(f[f"{i}"]-v).argmin()
    colidx=f.columns.get_indexer([f"{i}"])[0]
    q=f.iloc[rowidx,colidx:colidx+5]
    q.name="date"
    if test:
        print(f"{q[4]*100:.2f}% ({rowidx=}, {colidx=})")
    return q


# params
i="ng"
p=f"{i}zsprng"
_pctrng=(.3,99.7)
_prbrng=(.03,5)
_color="deep"

# execution
f=getdata(local=False,roll=True,roll_n=3)
ff=zs(f,pctrng=_pctrng)
fff=prbrng(ff,i,dropna=False)

#visualisation
q=input(f"visualise?: ")
if q=="y" or q=="Y":
    hm(ff[["fsi","cys","5yi","10yt","wti","ng","zs","hg"]],
        corner=True,
        minmax=(-1,1),
        title=f"{_pctrng[0]}-{_pctrng[1]}")

    fx=f.interpolate(method="time")
    x=sns.pairplot(f,
        vars=["wti","hg","zs","ng","cys","fsi","10yt"],
        hue=None,
        dropna=False,
        kind="scatter",
        diag_kind="hist",
        palette=_color,)
    x.map_diag(sns.histplot,multiple="stack",element="step")

    sns.relplot(ff,x="30ym",y="zs",
        hue=None,palette=_color,
        size="wti",sizes=(1,150))

    fg,ax=plt.subplots(1,3,figsize=(12,12))
    fg.suptitle("da_ed")

# sns.kdeplot(fs0Tot["ng"],x="ng")
# sns.displot(fs0Tot["ng"],x="ng",bins=10)
