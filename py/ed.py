import numpy as np
import pandas as pd
import seaborn as sns
from full_fred.fred import Fred as fed

FRED_API_KEY="c:/code/fed"

codes={
    "fsi":"STLFSI3",
    "cys":"BAMLH0A0HYM2",
    "5yi":"T5YIE",
    "ng":"DHHNGSP",
    "wti":"DCOILWTICO",
}

def sanitize(frame):
    for col in frame.columns:
        frame[col][frame[col]=="."]=np.nan
    return frame

fed=fed(FRED_API_KEY)

frames={code:fed.get_series_df(codes[code]).loc[:,"date":] for code in codes}

for frame in frames:
    frames[frame].columns=["date",frame]
    frames[frame]=frames[frame].set_index("date")
    frames[frame].index=pd.to_datetime(frames[frame].index,yearfirst=True)

frame_chk=pd.concat(frames.values())
frame_org=(pd.DataFrame(
    pd.date_range(frame_chk.index.min(),frame_chk.index.max()),columns=["date"])
    .set_index("date"))
frame_tot=[q for q in frames.values()]
frame_rslt=frame_org.join(frame_tot,how="left")
frame_rslt=(sanitize(frame_rslt).astype("float").interpolate("linear"))

frame_rslt_info=frame_rslt.describe()

for col in frame_rslt.columns:
    val_col_max=frame_rslt[col].min()

sns.kdeplot(data=frame_rslt,x="ng")
sns.displot(frame_rslt,x="ng",bins=10)