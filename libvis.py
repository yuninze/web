import time as t
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

rg=np.random.default_rng(9405)
xy=pd.DataFrame(rg.gamma(100,size=(1000,10)),columns=[q for q in range(10)])

def pre_req():
    fig,ax=plt.subplots(figsize=(5,8))
    sns.set_theme("white")

def quick_visual_bp(data,x,y):
    sns.boxplot(data=data,x="col0",y="col1")
    plt.xlabel(f"{col0.name}")
    plt.ylabel(f"{col1.name}")
    plt.title(f"{p}")
    ax.set(xticklabels=["col0Explanation","col1Explanation"])

###Basic visualizing
#for numeric data
sns.pairplot(xy,hue="f{categorizable/indexable_data_label}",diag_kind="hist")
#The innermost EDAs for
sns.pairplot(xy,x_vars=[],y_vars=target_vars,size=4,aspect=1,kind="scatter")
plt.show(block=0)


#check data type is array-like
type(xy)
#get correlation
xy_corr=xy.corr()
#have mask, boolVec2int
mask=np.triu(np.ones_like(xy_corr,dtype=bool))
#
sns.set_theme(style="whitegrid",font="monospace")
#
cmap=sns.diverging_palette(4,155,as_cmap=True)
#cmap=sns.color_palette("light:#5A9",as_cmap=True)

#
sns.heatmap(xy_corr,mask=mask,cmap=cmap,annot=True,center=0,square=True,
linewidths=.5,fmt=".3f",ax=ax)

df.groupby('qtr').agg({"realgdp": ["mean",  "std"], "unemp": "mean"})
fig, ax = plt.subplots(figsize=(5, 8))
sns.boxplot(data=life_time_df, x='user_churn', y='max(life_time)')
plt.xlabel('User Churn')
plt.ylabel('Time Since Registration')
plt.title('Time since registration and churn')
ax.set(xticklabels=['Not Churned', 'Churned'])

f,ax=plt.subplots(figsize=(13,9))
x=pd.DataFrame(np.random.rand(10,3),columns=list("abc"))
s=(20*np.random.rand(x.shape[0]))**2
c=(np.random.rand(x.shape[0]))
ax,fig=plt.subplots(figsize=(10,7))
plt.scatter(x.a,x.b,s=s,c=c,alpha=0.5)