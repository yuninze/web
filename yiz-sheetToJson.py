import os,csv,json
import pandas as pd
import numpy as np
from collections import OrderedDict
os.chdir('z:\\FRIEND\\yun_work\\code\\')
sheet0=pd.read_excel('wirelink.xlsx',sheet_name=[1],index_col=None,header=0)
sheet1=pd.read_excel('wirelink.xlsx',sheet_name=[2],index_col=None,header=0)
sheet2=pd.read_excel('wirelink.xlsx',sheet_name=[3],index_col=None,header=0)
df=pd.DataFrame(columns=['type','id','badword','goodword'])

for a in range(len(sheet0[1])):df[0][a]=sheet0[1]['분류'][a]
for a in range(len(sheet0[1])):df[1][a]=sheet0[1]['일련번호(메뉴/페이지명)'][a]
for a in range(len(sheet0[1])):df[2][a]=sheet0[1]['문제 용어'][a]
for a in range(len(sheet0[1])):df[3][a]=sheet0[1]['권장 용어(고객 관점 언어)'][a]
print(df)
