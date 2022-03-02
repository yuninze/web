zyeon
zyeon=pd.pivot_table(a,values='money',index=['idx','name','cn','wm'],aggfunc=np.sum)
zyeon.unstack().to_csv('zyeon.csv',encoding='utf-8-sig')

fileobject
a=concoction('C:/code/concat/ca',10,10)
b=concoction('C:/code/concat/cz',10,10)
c=concoction('C:/code/concat/la',560,70)
d=concoction('C:/code/concat/lz',560,70)
e=concoction('C:/code/concat/nla',560,70)
fs=[a,b,c,d,e]
f=sansibar(fs,pii='C:/code/concat/pii.csv')

np.iinfo(obj)
np.finfo(obj)
pd.interval_range()
pd.cut(x=series,bin=rangearray)

100Ка(100УЪ)
r"\((\d+.\d+).\)"
@*
^\S+@\S+$

labels = ["{0} - {1}".format(i, i + 9) for i in range(0, 100, 10)]

items = [
    tuple(func(y) if i == level else y for i, y in enumerate(x)) for x in self
]


ca=concoction('C:/82/stat/concat/ca',10,10)
cz=concoction('C:/82/stat/concat/cz',10,10)
la=concoction('C:/82/stat/concat/la',70,550)
lz=concoction('C:/82/stat/concat/lz',70,550)

import csv

with open('c:/filenamelist.csv',encoding='utf-8',newline='',mode='w+') as filenamelistcsvfile:
	csvwriter=csv.writer(filenamelistcsvfile);[csvwriter.writerow([t]) for t in filenamelist]

with open('c:/dataidxlist.csv',encoding='utf-8',newline='',mode='w+') as dataidxlistcsvfile:
	csvwriter=csv.writer(dataidxlistcsvfile);[csvwriter.writerow([t]) for t in dataidxlist]

위반 이미지파일 개수, 위험 이미지파일 개수, 정상 이미지파일 개수
정상 이미지파일 개수=전체 개수-(위반 이미지파일 개수+위험 이미지파일 개수)

ArcNameList=ZipFile('PRJ3668.zip').namelist()
ArcNameListJsonfile=[x for x in ArcNameList if '.json' in x]
ArcNameListing=[x for x in ArcNameList if '.jpg' in x]
ArcNameListingSon={}
ArcNameListingSon['aw']=[h for h in ArcNameListing if 'IMAGE/A/WHITE/' in h]
ArcNameListingSon['ay']=[h for h in ArcNameListing if 'IMAGE/A/YELLOW/' in h]
ArcNameListingSon['ab']=[h for h in ArcNameListing if 'IMAGE/A/BLUE/' in h]
ArcNameListingSon['as']=[h for h in ArcNameListing if 'IMAGE/A/SHOULDER/' in h]
ArcNameListingSon['bw']=[h for h in ArcNameListing if 'IMAGE/B/WHITE/' in h]
ArcNameListingSon['by']=[h for h in ArcNameListing if 'IMAGE/B/YELLOW/' in h]
ArcNameListingSon['bb']=[h for h in ArcNameListing if 'IMAGE/B/BLUE/' in h]
ArcNameListingSon['bs']=[h for h in ArcNameListing if 'IMAGE/B/SHOULDER/' in h]
ArcNameListingSon['cw']=[h for h in ArcNameListing if 'IMAGE/C/WHITE/' in h]
ArcNameListingSon['cy']=[h for h in ArcNameListing if 'IMAGE/C/YELLOW/' in h]
ArcNameListingSon['cb']=[h for h in ArcNameListing if 'IMAGE/C/BLUE/' in h]
ArcNameListingSon['cs']=[h for h in ArcNameListing if 'IMAGE/C/SHOULDER/' in h]
for x,y in ArcNameListingSon.items():print(f'{x}: {len(y)}')

frame1=pd.read_csv('c:/82_stats_fuck.csv',nrows=5000,encoding='utf-8-sig',low_memory=False)

from libtype import *
cw=pd.read_csv('cw.csv')
cw.cn=cw.cn.apply(dashingcn)
cw.pn=cw.pn.apply(dashingpn)
cw.money=cw.money.apply(accountingtostr)
cw.set_index(['name','cn','pn'],inplace=True)
	
	
frame3=frame2[pd.isna(frame2.성명)]
for i in frame3.index:
	frame3.loc[i,'name']=str(i)[:3]
	frame3.loc[i,'cn']=str(i)[3:]

frame0.set_index(inplace=True)
fuck=pd.pivot_table(frame0,values='money',index=['name','wm'])
fuck.unstack()

half
float16
single
float32
double
float64

for fuck in d.index:
    col=d.loc[fuck]
    row=col.loc["variety"]
    if "장애" in row:
        col.loc["zangae"]="O"
    elif "임신" in row:
        col.loc["preg"]="O"
    elif "단절" in row:
        col.loc["gzy"]="O"
    elif "보훈" in row:
        col.loc["bohun"]="O"
    elif "다문화" in row:
        col.loc["damunwha"]="O"
    elif "초등" in row:
        col.loc["choding"]="O"
    elif "대학생" in row:
        col.loc["daeding"]="O"
    elif "투잡" in row:
        col.loc["jobtwo"]="O"
    elif "미취업자" in row:
        col.loc["jobno"]="O"
    elif "실직자" in row:
        col.loc["jobloss"]="O"
    elif "저소득" in row:
        col.loc["lowincome"]="O"
    elif "장기실업" in row:
        col.loc["jobless"]="O"
    elif "가장" in row:
        col.loc["mobuzang"]="O"
    elif "이주" in row:
        col.loc["visamarry"]="O"
    elif "북한" in row:
        col.loc["bukhan"]="O"
    elif "자영업" in row:
        col.loc["selfempoly"]="O"
    elif "AI" in row:
        col.loc["aihubhx"]="O"

def queuing():
arc=ZipFile(zipfile,"r")
infolist=arc.infolist()
arcnamelist=[infolist[x] for x in range(len(infolist)) if infolist[x].endswith(".jpg")]

queuing by genComp

factor=2000

blockcount=len(donefilename)//factor
blocknumber=len(donefilename)%factor
blockindex=0

donefilenamelist=[]
donefilenameblock=dict()

for x in range(blockSize)
    [blockindex:blockcontent for blockindex,blockcontent in range(blockcount),
    [donefilenamelist for x in range(blockSize 