import numpy as np
import pandas as pd
import seaborn as sns
import scipy.stats
from full_fred.fred import Fred

pd.options.display.min_rows=20
pd.options.display.float_format=lambda q:f"{q:%.3f}"

# basic checks
# df[columns].dtypes
# df[columns].memory_usage(deep=1)

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
    "ri":"RECPROUSM156N"
}

def sanitize(f):
    for col in f.columns:
        f[col][f[col]=="."]=np.nan
    return f

fed=Fred(fredkey)
fs0={id:fed.get_series_df(ids[id]).loc[:,"date":] for id in ids}

for f in fs0:
    fs0[f].columns=["date",f]
    fs0[f]=fs0[f].set_index("date")
    fs0[f].index=pd.to_datetime(fs0[f].index,yearfirst=True)
f0=[q for q in fs0.values()]

f1=pd.concat(fs0.values())
f2=(pd.DataFrame(
    pd.date_range(f1.index.min(),f1.index.max()),columns=["date"])
    .set_index("date")) # for full-range datetime indices

# join takes series,iterables,dataframes
f3=f2.join(f1,how="left")
f3=sanitize(f3).astype("float")
f3i=f3.describe()

# na-dropped, zscored
fs1={}
for col in f3.columns:
    target=f3[col].dropna()
    mm=np.percentile(target,[1,99])
    target[(target<=mm[0])|(target>=mm[1])]=np.nan,fs1.append(target)
    fs1[col]=pd.concat([target,
        scipy.stats.zscore(target,nan_policy="omit")],axis=1)
    fs1[col].columns=[f"{col}",f"{col}_zs"]

fs0Tot=fOrg.join([q for q in fs0.values()],how="left") 
fs1Tot=fOrg.join(fs1,how="left")

fs1Tot["ngZsRng"]=np.where(
(abs(fs0Tot["ng_zs"])<=1),"q<=1",fs1Tot["ngZsRng"])
fs1Tot["ngZsRng"]=np.where(
(abs(fs0Tot["ng_zs"])>1) & (abs(fs0Tot["ng_zs"])<=2),
"1<q<=2",fs1Tot["ngZsRng"])
fs1Tot["ngZsRng"]=np.where(
(abs(fs0Tot["ng_zs"])>2),
"q>2",fs1Tot["ngZsRng"])

scipy.stats.norm.ppf({target_prob})->zscore
scipy.stats.norm.cdf({zscore})->target_cum_prob

sns.kdeplot(fs0Tot["ng"],x="ng")
sns.displot(fs0Tot["ng"],x="ng",bins=10)
