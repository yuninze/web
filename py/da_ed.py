from glob import glob
import numpy as np
import pandas as pd
import scipy.stats
from full_fred.fred import Fred

pd.options.display.min_rows=8
pd.options.display.float_format=lambda q:f"{q:.10f}"

def full_range_idx(f:pd.DataFrame,test=False):
    if test:# frame with full-range date indices
        return np.arange(
            f.index.min(),f.index.max(),dtype="datetime64[D]")
    return (pd.DataFrame(
        pd.date_range(
            f.index.min(),f.index.max()),columns=["date"])
            .set_index("date"))

def messij(f:pd.DataFrame)->pd.DataFrame:
    return f.apply(pd.to_numeric,errors="coerce")

def prbrng(f:pd.DataFrame,id:str,rng=6,
    test=False)->pd.DataFrame:
    if not id in f.columns:
        raise NameError(f"{id} not exist in columns")
    
    colp=f"{id}zsprb"
    rng=np.flip(np.geomspace(.05,1,rng))[1:]
    f.loc[:,f"{colp}rng"]=None
    for q in range(len(rng)):
        f.loc[:,f"{colp}rng"]=np.where(
            (f[colp]<=rng[q])&(~pd.isna(f[colp])),
            f"{rng[q]}",f[f"{colp}rng"])
    
    return f.dropna(subset=f"{colp}rng")
    # isna(colp) is worthless

local=True
prbrngtgt="wti"

if local:
    f=(pd.read_csv("c:/code/data0.csv",
        index_col="date",
        converters={"date":pd.to_datetime},
        na_filter=False)
        .apply(pd.to_numeric,errors="coerce"))
    print("success: got local")

else:
    int={
        "fsi":"STLFSI3",
        "cys":"BAMLH0A0HYM2",
        "5yi":"T5YIE",
        "ng":"DHHNGSP",
        "wti":"DCOILWTICO",
        "30ym":"MORTGAGE30US",
        "ri":"RECPROUSM156N",
        "nfp":"ADPWNUSNERSA",
        "10yt":"DGS10"
    }
    ext={
        "zs":"soybean",
        "hg":"copper"
    }
    fed=Fred("c:/code/fed")
    fs={id:fed.get_series_df(int[id])
        .loc[:,"date":]
        .astype({"date":"datetime64[ns]"})
        .set_index("date")
        .rename(columns={"value":id}) for id in int}
    print("success: got fred")

    fsincsv=[pd.read_csv(q,
        index_col="date",
        converters={"date":pd.to_datetime},
        na_filter=False) for q in sorted(glob(r"c:/code/da_**.csv"))]
    if not len(fsincsv)==len(ext):
        raise IndexError("csv read error")

    for q in range(len((fsincsv))):
        fs[f"{fsincsv[q].columns[0]}"]=fsincsv[q]

    f=messij(pd.concat(fs.values(),axis=1))
    f.to_csv("c:/code/data0.csv",encoding="utf-8-sig",)

fcache=[]
for id in f.columns:
    q=f[id].dropna()
    mm=np.percentile(q,(0.3,99.7))
    q[(q<=mm[0])|(q>=mm[1])]=np.nan
    zs=scipy.stats.zscore(q,nan_policy="omit")
    zsprb=pd.DataFrame(
        1-scipy.stats.norm.cdf(zs),index=zs.index)
    w=pd.concat([q,pd.concat([zs,zsprb],axis=1)],axis=1)
    w.columns=[f"{id}",f"{id}zs",f"{id}zsprb"]
    fcache.append(w)

ff=full_range_idx(f).join(pd.concat(fcache,axis=1),how="left")
ff.to_csv("c:/code/data1.csv",encoding="utf-8-sig",)

# resampling
fff=prbrng(ff,prbrngtgt,rng=5)

def eli(a,v)->tuple:
    """array-like, value"""
    i=np.abs(a-v).argmin()
    return (i,a[i])

def waratah(a,i,id)->str:
    """array-like, index of value, product id"""
    ic=a.columns.get_indexer([f"{id}"])[0]
    q=a.iloc[i,ic:ic+3]
    print(f"{q[2]:.5f}%")
    return q

hm(fff[["fsi","cys","5yi","30ym","10y","wti","ng","zs","hg"]],
corner=True,minmax=(-1,1),
title="0.3-99.7,non-interpolated")

# sns.kdeplot(fs0Tot["ng"],x="ng")
# sns.displot(fs0Tot["ng"],x="ng",bins=10)

tgt=prbrngtgt
waratah(fff,eli(f[f"{tgt}"],85.5)[0],id=tgt)
eli(fff[f"{tgt}"],85.5)
