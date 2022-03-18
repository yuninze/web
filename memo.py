df.replace("nan",np.nan)
df.loc[q,w] for q in df.index for w in df.columns

conditional listdir보다 scandir이 3배 빠름
scandir->os.DirEntry
os.scandir.close()
os.DirEntry.name
os.DirEntry.path
os.DirEntry.is_dir()
os.DirEntry.is_file()
os.DirEntry.stat.st_size

A=12345
if A>=500:

Working set is a concept in computer science which defines the amount of 
memory that a process requires in a given time interval.

import pandas as pd
iinfo(obj)
finfo(obj)
pd.interval_range()
pd.cut(x=series,bin=rangearray)
quantile(
    q=arrayAlike,
    axis=matrixWise,
    interpolation=
)

pd.to_datetime(
(arg:1-d array,series,dataframe,dict-like),
yearfirst=,
format="%Y/%d/%m/"
infer_datetime_format=False,
origin=parseableDatetime
unit=parseBasisUnit

pd.to_datetime(target)

pd.Timestamp()

#returns containing-subset
where((bool Series/DataFrame, array-like, or callable),other=,axis=)
#inverse boolean of where
mask((bool Series/DataFrame, array-like, or callable),other=,axis=)

pd.DataFrame.from_dict(
    data=dict,
    orient='index')
orient index, keys to rows (index)
oirent columns, keys to columns (columns)
orient: location of keys


select_dtypes(inc=,exc=)


more than 10_000 rows
eval()->boolVec
query()->satisfying rows
parser가 거의 가틍ㅁ

noMoreRegex
int(''.join([q for q in STRING if q.isdigit()]))

100Ка(100УЪ)
r"\((\d+.\d+).\)"
@*
^\S+@\S+$

["rangeLabelGen {0}-{1}".format(q,q+10) for q in range(0,10000,10)]
ijk
start stop step
[i:j:k]
items = [tuple(func(y) if i == level else y for i, y in enumerate(x)) for x in self]
{"key_"+a+b:"val_"+a+b for a,b in {a+b:a+b for a in "abcd" for b in "0123" if "a"!="b"}.items()}

Working binning
데.누.방.
Bin Width 검증하기, 어떻게 supervised binning

f_sexage=pd.DataFrame(list(map(getsexage,f.cn.values)))
f['sex']=f_sexage.iloc[:,0].to_numpy()
f['age']=f_sexage.iloc[:,1].to_numpy()
*map(getmd,f.index.get_level_values(0)),

Fixation binning
frame['agerng']=pd.cut(x=frame.age,bins=pd.interval_range(start=0,end=110,periods=10)).to_numpy()
frame.column.quantile(q=x)->np.float64

pd.qcut(x=f.work,q=(0,.5,.6,.7,.75,.8,.85,.9,.95,1.))

f['TErng']=pd.cut(x=f.TE,bins=pd.interval_range(start=0,end=f.TE

Entropy binning for workrng, TErng
frame['wrkrng']=pd.cut(x=frame.age,bins=pd.interval_range(start=0,end=110,periods=10)).to_numpy()

annot=True,fmt='d',linewidths=.1,cmap='plasma'

ax=sns.heatmap(atc1,annot=True,fmt='d',linewidths=.5,cmap='viridis',vmax=500)
atc.groupby('usersex')['paytimerng'].value_counts()

ax4=ax4[ax4>0].dropna(axis=0,how='all')
a0[np.isnan(a0[~np.isnan(a0)])]=0

xticklabels
yticklabels

NaN, NaT, null, 0, ''
pd.isna
>>> pd.isnull
<function isna at 0x7fb4c5cefc80>
pd.notna->i.b.
>>> pd.isnull
<function isna at 0x7fb4c5cefc80>
np.isnan->ufunc

np.triu(mat,k:int)
np.tril(mat,k:int)
k-th diagonal, starting from the main diagonal of a matrix A is the list of entries 
A_{i, j} where i=j.
All off-diagonal elements are zero in a diagonal matrix.

broadcasting
at least one axes should have same length
l transformat


e.g.
for q in target0.columns:
	scalarsum=sum(target0[q])
	target0[q]=target0[q]/scalarsum

for q in range(len(target.index)):
	scalarsum=sum(target.iloc[q,:])
	target.iloc[q,:]=target.iloc[q,:]/scalarsum

cache=[]
with open('namu.json',encoding='utf-8') as jsonfile:
	for q in range(100):
		cache.append(json.loads(jsonfile.readline()))

	
	
	
fileobject
a=concoction('C:/code/concat/ca',10,10)
b=concoction('C:/code/concat/cz',10,10)
c=concoction('C:/code/concat/la',560,70)
d=concoction('C:/code/concat/lz',560,70)
e=concoction('C:/code/concat/nla',560,70)
fs=[a,b,c,d,e]
f=sansibar(fs,pii='C:/code/concat/pii.csv')
	


zyeon
zyeon=pd.pivot_table(a,values='money',index=['idx','name','cn','wm'],aggfunc=np.sum)
zyeon.unstack().to_csv('zyeon.csv',encoding='utf-8-sig')

np.iinfo(obj)
np.finfo(obj)
pd.interval_range()
pd.cut(x=series,bin=rangearray)

100Ка(100УЪ)
r"\((\d+.\d+).\)"
@*
^\S+@\S+$


items = [
    tuple(func(y) if i == level else y for i, y in enumerate(x)) for x in self
]

Working binning
데.누.방.
Bin Width 검증하기, 어떻게 supervised binning

f_sexage=pd.DataFrame(list(map(getsexage,f.cn.values)))
f['sex']=f_sexage.iloc[:,0].to_numpy()
f['age']=f_sexage.iloc[:,1].to_numpy()
*map(getmd,f.index.get_level_values(0)),

Fixation binning
frame['agerng']=pd.cut(x=frame.age,bins=pd.interval_range(start=0,end=110,periods=10)).to_numpy()
frame.column.quantile(q=x)->np.float64

pd.qcut(x=f.work,q=(0,.5,.6,.7,.75,.8,.85,.9,.95,1.))

f['TErng']=pd.cut(x=f.TE,bins=pd.interval_range(start=0,end=f.TE

Entropy binning for workrng, TErng
frame['wrkrng']=pd.cut(x=frame.age,bins=pd.interval_range(start=0,end=110,periods=10)).to_numpy()



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

frame1=pd.read_csv('c:/82_stats.csv',nrows=5000,encoding='utf-8-sig',low_memory=False)

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
pd.pivot_table(frame0,values='money',index=['name','wm'])
unstack()

half
float16
single
float32
double
float64

def queuing():

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