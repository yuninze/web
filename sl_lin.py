import numpy as np
import pandas as pd
from time import time as t
from sklearn.datasets import make_blobs
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import (
    StandardScaler,OneHotEncoder)
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import (
    SelectKBest,chi2,VarianceThreshold)
from sklearn.linear_model import (
    LinearRegression,LogisticRegression)
from scipy.stats import (
    ttest_1samp,ttest_ind,chi2_contingency)

#removable blocks
def captivate(type="r",size=1000,seed=94056485):
    if type=="blob":
        return make_blobs(n_samples=size,
        n_features=4,random_state=seed)
    else:
        seed=np.random.default_rng(seed)
        if type=="gamma":
            rg=seed.gamma(1,size=(size,4))
        elif type=="int":
            rg=seed.integers(100,size=(size,4))
        elif type=="rand":
            rg=seed.random(size=(size,4))
        else:
            rg=seed.uniform(0,100,size=(size,4))
        return pd.DataFrame(rg,
            columns=list("abcd"))

def prep(q):
    q["prep0"]=(q
        .select_dtypes(include="number")
        .sum(axis=1)
        .copy())
    q["prep1"]=(np.where(
        q["prep0"]>np.mean(q["prep0"]),"large","small"))
    return q

def see_cat(q):
    #df[df.catCol==df.catCol.cat.categories[x]]
    return [q for q in q.cat.categories]

def have_rng(q,var_name,q_num=4):
    if isinstance(q,(pd.DataFrame,pd.Series)):
        q[f"{var_name}_rng"]=pd.qcut(var_name,q=q_num,labels=None)
        return q
    raise TypeError(f"{type(q)=}")

#very high level interfaces
def clar(q,cat=False,w=None,m=None,rg=None):
    if not cat:
        if m:
            r=ttest_1samp(q,popmean=m)
            print(f"{r.pvalues:.5f}")
            return r
        else:
            if not q.shape[0]==w.shape[0]:
                row_cnt=min(q.shape[0],w.shape[0])
                print(f"resampled: {row_cnt}")
                q,w=[e.sample(n=row_cnt,random_state=rg) for e in (q,w)]
                r=ttest_ind(q,w)
            print(f"{r.pvalues:.5f}")
            return r
    r=chi2_contingency(q)
    if isinstance(q,pd.Series):
        name=q.name
        klas=pd.Series
    else:
        name=q.columns.values
        klas=pd.DataFrame
    return {"chi2":f"{r[0]:.5f}",
        "p":f"{r[1]:.5f}",
        "dof":f"{r[2]:.5f}",
        "exp":klas(r[3],
        index=q.index.values,columns=name)}

def selfea(q,w=None,m=chi2,f_num=1,p=.9):
    '''q:data,w:target_var'''
    #VarianceThreshold for numerics
    #larger variance, higher k-score
    if m==VarianceThreshold:
        var=p*(1-p)
        #as fit results disregards w:y
        #this returns VT cursor directly
        return (m(threshold=var)
            .fit(q))
    else:
        if not w is None:
    #lower pvalues would get higher k-score
            return (SelectKBest(score_func=m,k=f_num)
                .fit(X=q,y=w))
    raise TypeError(f"performing SelKBest but y:{w=}")

def regres(data,y,ccols=None,type="con"):
    #removable block
    if not isinstance(data,pd.DataFrame):
        return f"aceepts pd.DataFrame"
    if not y in data.columns:
        return f"y is not existing in the data"
    #customization
    x=list(set(data.columns)-{y})

    #numeric data pipeline
    #scaling, standardazation
    #standardize features by removing
    #the mean and scailing to unit variance
    #make_pipeline
    ncols=x
    nt_si_ss=Pipeline(steps=[
        #Interpolation, imputation, scaling
        #mean substitution, NMF, regression
        #SimpleImputer(missing_values=np.nan|target value
        #strategy="mean","median","most_frequent","constant",
        #fill_value:if strategy "constant" -> str,verbose=0)
        ("imputer",SimpleImputer(strategy="median")),
        ("scaler",StandardScaler(with_mean=True))])

    #cat. data pipeline
    if type=="bin" and ccols is None:
        return f"specify categorical feature column label"
    ccols=[]
    ct_ohe=Pipeline(steps=[
        ("ohe",OneHotEncoder(handle_unknown="ignore"))])

    #preprocessor without ccols
    pp=ColumnTransformer(transformers=[
        ("nt",nt_si_ss,ncols),("ct",ct_ohe,ccols)])

    if type=="bin":
        lr=Pipeline(steps=[
            ("pp",pp),
            ("logr",LogisticRegression(n_jobs=-1))])
    elif type=="con":
        lr=Pipeline(steps=[
            ("pp",pp),
            ("linr",LinearRegression(n_jobs=-1))])
    else:
        return None

    #split
    x0,x1,y0,y1=train_test_split(data[x],data[y],
        test_size=.1,random_state=True)

    t0=t()
    #fitting
    lr.fit(x0,y0)
    print(f"fitted. elasped {t()-t0:.5f}s")
    #get R**2
    if len(x1)==len(y1):
        print(f"R**2: {lr.score(x1,y1):.5f}")
    return lr
#cross_val_score(a,tokenData,targetData,cv=?)