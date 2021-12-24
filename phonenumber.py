import os
import pandas as pd

os.chdir("c:\\")
df=pd.read_csv("csv.txt",encoding="utf-8-sig")

for x in df.index:
    df.iloc[x,"number"]=df.iloc[x,"number"].
