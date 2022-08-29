import numpy as np
import pandas as pd
import seaborn as sns
from full_fred.fred import Fred as fed
from scipy.stats import zscore

pd.set_option("display.float_format",lambda q:f"{q:%.4f}")

FRED_API_KEY="c:/code/fed"

codes={
    "fsi":"STLFSI3",
    "cys":"BAMLH0A0HYM2",
    "5yi":"T5YIE",
    "ng":"DHHNGSP",
    "wti":"DCOILWTICO",
}

# join gets series,iterables,dataframes

def sanitize(frame):
    for col in frame.columns:
        frame[col][frame[col]=="."]=np.nan
    return frame

fed=fed(FRED_API_KEY)
fs={code:fed.get_series_df(codes[code]).loc[:,"date":] for code in codes}

for f in fs:
    fs[f].columns=["date",f]
    fs[f]=fs[f].set_index("date")
    fs[f].index=pd.to_datetime(fs[f].index,yearfirst=True)
fTot=[q for q in fs.values()]

fChk=pd.concat(fs.values())
fOrg=(pd.DataFrame(
    pd.date_range(fChk.index.min(),fChk.index.max()),columns=["date"])
    .set_index("date"))

fRst=fOrg.join(fTot,how="left")
fRst=sanitize(fRst).astype("float")
fRstIfo=fRst.describe()

fs0={}
fs1=[]
for col in fRst.columns:
    target=fRst[col].dropna()
    mm=np.percentile(target,[1,99])
    target[(target<=mm[0])|(target>=mm[1])]=np.nan
    fs1.append(target)
    fs0[col]=pd.concat([target,zscore(target,nan_policy="omit")],axis=1)
    fs0[col].columns=[f"{col}",f"{col}_zs"]

fs0Tot=fOrg.join([q for q in fs0.values()],how="left") # 1-99 with zscores
fs1Tot=fOrg.join(fs1,how="left") # 1-99
# pairplotting, coloring by zscore range
# zscores recalc is not needed by nan_policy

ng=fs0["ng"]
print(ng[(ng["ng_zs"]>3)|(ng["ng_zs"]<-3)])

sns.kdeplot(frame_rslt,x="ng")
sns.displot(frame_rslt,x="ng",bins=10)