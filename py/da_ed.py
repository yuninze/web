import numpy as np
import pandas as pd
import scipy.stats
from full_fred.fred import Fred

pd.options.display.min_rows=10
pd.options.display.float_format=lambda q:f"{q:.5f}"

# df[idumns].dtypes
# df[idumns].memory_usage(deep=1)

fredkey="c:/code/fed"

class ed:
    def __init__(self,f,n,id):
        self.content=f
        self.name=n
        self.id=id
        self.des=f.describe()
    def zs(self):
        return scipy.stats.zscore(self.content[self.id])

ids={
    "fsi":"STLFSI3",
    "cys":"BAMLH0A0HYM2",
    "5yi":"T5YIE",
    "ng":"DHHNGSP",
    "wti":"DCOILWTICO",
    "30ym":"MORTGAGE30US",
    "ri":"RECPROUSM156N",
    "nfp":"ADPWNUSNERSA"
}

def sanitize(f):
    for id in f.columns:
        f[id][f[id]=="."]=np.nan
    return f

def truthy(*vals):
    for x in vals:
        if not x:
            raise SystemExit(f"{x}")

fed=Fred(fredkey)
fs0={id:fed.get_series_df(ids[id]).loc[:,"date":] for id in ids}

for id in fs0:
    fs0[id].columns=["date",id]
    fs0[id]=fs0[id].set_index("date")
    fs0[id].index=pd.to_datetime(fs0[id].index,yearfirst=True)

f0=[q for q in fs0.values()]

f1=pd.concat(fs0.values(),axis=1)
f2=(pd.DataFrame(
    pd.date_range(f1.index.min(),f1.index.max()),columns=["date"])
    .set_index("date"))# frame with full-range date indices

f3=f2.join(f1,how="left")# takes series,iterables,dataframes
f3=sanitize(f3).astype("float")
f3i=f3.describe()

# na-dropped, zscored
fs1={}
for id in f3.columns:
    target=f3[id].dropna()
    mm=np.percentile(target,(0.7,99.3))
    target[(target<=mm[0])|(target>=mm[1])]=np.nan
    zs=scipy.stats.zscore(target,nan_policy="omit")
    zsprb=pd.DataFrame(
        1-scipy.stats.norm.cdf(zs),index=zs.index)
    fs1[id]=pd.concat([target,pd.concat([zs,zsprb],axis=1)]
        ,axis=1)
    fs1[id].columns=[f"{id}",f"{id}zs",f"{id}zsprb"]

f4=f2.join([q for q in fs1.values()],how="left")

id=f"ng"
idzscolname=f"{id}zs" # not used
zsrng=f"{id}zsrng"

f4[zsrng]=None
f4[zsrng]=np.where(
(abs(f4[f"{id}zs"])<=1),"q<=1",f4[zsrng])
f4[zsrng]=np.where(
(abs(f4[f"{id}zs"])>1) & (abs(f4[f"{id}zs"])<=2),
"q>1",f4[zsrng])
f4[zsrng]=np.where(
(abs(f4[f"{id}zs"])>2),
"q>2",f4[zsrng])
f4[zsrng]=np.where(
(abs(f4[f"{id}zs"])>2.5),
"q>2.5",f4[zsrng])

try:
    if "nfp" in ids:
        f4.ng[~pd.isna(f4.ng)].index.intersection(f4.nfp[~pd.isna(f4.nfp)].index)
        f4.nfp.value_counts(dropna=False)
        f4.nfp[np.isnan(f4.nfp)]
        f4["nfp"]=f4["nfp"].interpolate()
        opt=("nfp","ri")
except:
    ...
else:
    idsdatacols=list(set(fs0.keys())-set(opt))
finally:
    f5=f4.dropna(subset=zsrng)
    f5=f5[idsdatacols+[zsrng]]

pp(f5,hue=zsrng,corner=False)
hm(f5,corner=True,minmax=(-1,1),title="0.7-99.3,dropna,non-interpolated")

# scipy.stats.norm.pdf({obs})
# scipy.stats.norm.ppf({target_prob})->zscore
# scipy.stats.norm.cdf({zscore})->target_cum_prob

# sns.kdeplot(fs0Tot["ng"],x="ng")
# sns.displot(fs0Tot["ng"],x="ng",bins=10)
