from typing import Iterable
from time import time as t
from collections import Counter
from seaborn import diverging_palette
from wordcloud import WordCloud
from konlpy.tag import Okt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

jvm="C:/Program Files/Java/jdk-18/bin/server/jvm.dll"
font="C:/code/base/GBR.ttf"
output_imgfile="wc.png"

def prac():
    return 0
    #set vectorizer
    cursor=CountVectorizer()
    #fit source
    data=cursor.fit_transform(corpus)
    #get analyzer as target
    anal=cursor.build_analyzer()
    #get feature names
    cursor.get_feature_names_out()
    #CSR matrix to ndarray
    data.toarray()
    #get column index of specific feature
    cursor.vocabulary_.get("정신")

def gdstrb()->tuple:
    return tuple(np.random.default_rng().integers(0,255,size=3))

def get_txt(txtfile=None)->str:
    if not txtfile:
        txtfile=input("txtfile: ")
    #by with statement, close() isn't needed
    with open(txtfile,encoding="utf-8") as txtfile:
        #return str immediately
        return txtfile.read()

def l2_scaler(i,l):
    i=np.array(i,dtype=np.float64)
    base=i.prod()**(1/l)
    return np.sqrt((i-base)**2)

def chk_map_dict_mean(map:dict):
    return sum([q for q in map.values()])/len(map)

def stdev(ob:Iterable):
    if isinstance(ob,Iterable):
        mean="mean"
        #foreach (observation - mean ** 2) sum divided by len(iterable)
        return np.sqrt(sum([(q-mean)**2 for q in ob])/len(ob))
    raise TypeError(f"{type(ob)}")

def noun_freq(text,
    l_noun=2,
    n_noun=500,
    norm=True,
    factor=1)->dict:
    t0=t()
    okt=Okt(jvmpath=jvm)
    noun=okt.nouns(text)
    noun=Counter([q for q in noun if len(q)>=l_noun])
    noun_map={q:w*factor for q,w in noun.most_common(n_noun)}
    if norm:
        noun_map_len=len(noun)
        noun_map_base=[noun_map[q] for q in noun_map.keys()]
        noun_map_dist=l2_scaler(noun_map_base,noun_map_len)
        noun_f={q:w for q,w in zip(noun_map.keys(),noun_map_dist)}
    print(f"noun_freq: elapsed in {t()-t0:.4f}s")
    return noun_f or noun_map

def quick_visual(occur_data):
    t0=t()
    if not isinstance(occur_data,pd.DataFrame):
        if isinstance(occur_data,dict):
            data=pd.DataFrame.from_dict(occur_data,
                orient="index",
                columns=["freq"])
        else:
            raise NotImplementedError(f"{type(occur_data)=}")
    plot=data.plot(kind="bar",rot=50,figsize=(20,15),
        title="noun_freq_map_chk",
        xlabel="noun_name",ylabel="noun_freq")
    plot.get_legend().remove()
    print(f"quick_visual: elapsed in {t()-t0:.4f}s")
    plt.show()

def make_wcld(f_noun,
    wc_font=font,
    wc_size=(1000,1000),
    wc_mask=None,wc_oval_shape=True,wc_mask_factor=.95,
    wc_cmap=diverging_palette(240,10,as_cmap=True),
    wc_bgcolor=None,
    wc_output_imgfile=output_imgfile,
    wc_output_imgfile_mode="RGBA",
    show=False):
    t0=t()
    if wc_oval_shape:
        #ogrid result (n,1..),(1,n..),ndim2 array
        x,y=np.ogrid[:wc_size[0],:wc_size[1]]
        #base coordinates for center
        wc_mask_base=sum(wc_size)/(len(wc_size)*2)
        #as x,y are ndarray, broadcasted
        #norm(x), norm(y) > norm(factor)
        wc_mask=((x-wc_mask_base)**2 + (y-wc_mask_base)**2 > 
                ((wc_mask_base*wc_mask_factor))**2)
        #bool2int to black(255) mask
        wc_mask=wc_mask.astype(int)*255
    wc=WordCloud(max_words=500,
        font_path=wc_font,
        height=wc_size[0],width=wc_size[1],
        mask=wc_mask,
        colormap=wc_cmap,
        background_color=wc_bgcolor,
        mode=wc_output_imgfile_mode,
        normalize_plurals=False,collocations=False)
    wc=wc.fit_words(f_noun)
    if wc_output_imgfile:
        wc.to_file(wc_output_imgfile)
    plt.imshow(wc,interpolation="bicubic")
    plt.axis("off")
    print(f"make_wcld: elasped in {t()-t0:.4f}s")
    if show:
        plt.show()
    return None

txt=get_txt("ko.txt")
n_freq=noun_freq(txt,n_noun=200,norm=True,factor=1)
make_wcld(n_freq,
    wc_bgcolor="black",wc_output_imgfile_mode="RGB",show=True)