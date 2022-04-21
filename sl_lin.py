import numpy as np
import pandas as pd
from time import time as t
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.model_selection import train_test_split

def captivate(seed=9405,type="gamma",size=1000):
    seed=np.random.default_rng(seed)
    if type=="gamma":
        rg=seed.gamma(100,size=(size,4))
    elif type=="int":
        rg=seed.randint(100,size=(size,4))
    else:
        rg=seed.random(size=(size,4))
    return pd.DataFrame(rg,
        columns=list("abcd"))

def regress(data,y,ccols=None,type="ren"):
    #removable block
    if not isinstance(data,pd.DataFrame):
        return f"aceepts pd.DataFrame"
    if not y in data.columns:
        return f"y is not existing in the data"
    #customization
    x=list(set(data.columns)-{y})
    #Interpolation, imputation, scaling
    ###imputation techniques: mean substitution, NMF, regression
    #SimpleImputer(missing_values=np.nan|target value
    #    strategy="mean","median","most_frequent","constant",
    #    fill_value:if strategy "constant" -> str
    #   verbose=0)
    ###Pipeline(steps=list of tuple(name,transform))
    ###Pipeline.named_steps: access the steps by name
    #numeric data pipeline
    ###scaling, standardazation
    ###standardize features by removing
    # the mean and scailing to unit variance
    ncols=x
    nt_si_ss=Pipeline(steps=[
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
    else:
        lr=Pipeline(steps=[
            ("pp",pp),
            ("linr",LinearRegression(n_jobs=-1))])

    #split
    x0,x1,y0,y1=train_test_split(data[x],data[y],
        test_size=.1,random_state=True)

    t0=t()
    #fitting
    lr.fit(x0,y0)
    print(f"fitted. elasped {t()-t0:.5f}s")

    #get R**2
    if len(x1)==len(y1):
        print(f"R2: {lr.score(x1,y1):.5f}")
    
    return lr
    #cross_val_score(a,tokenData,targetData,cv=?)