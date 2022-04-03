import numpy.random as nprnd
import numpy as np
import matplotlib.pyplot as plt
from typing import (Iterable)
from time import time as t
from collections import Counter
from wordcloud import WordCloud
from konlpy.tag import Okt

jvm="C:/Program Files/Java/jdk-18/bin/server/jvm.dll"
font="C:/code/base/GBR.ttf"
output_imgfile="wc.png"

def gdstrb()->tuple:
    return tuple(nprnd.default_rng().integers(0,255,size=3))

def get_txt(txtfile=None)->str:
    if not txtfile:
        txtfile=input("txtfile: ")
    #by with statement, close() isn't needed
    with open(txtfile,encoding="utf-8") as txtfile:
        #return str immediately
        return txtfile.read()

def l2s(i,l):
    i=np.array(i,dtype=np.float64)
    base=round(i.prod()**(1/l),5)
    dist=np.sqrt((i-base)**2)
    return dist

def noun_freq(text,l_noun=2,n_noun=500,f_multiplier=1.5,norm=True)->dict:
    t0=t()
    okt=Okt(jvmpath=jvm)
    noun=okt.nouns(text)
    noun=Counter([q for q in noun if len(q)>=l_noun])
    noun_map={q:w for q,w in noun.most_common(n_noun)}
    if norm:
        noun_map_len=len(noun)
        noun_map_base=[noun_map[q] for q in noun_map.keys()]
        noun_map_dist=l2s(noun_map_base,noun_map_len)
        noun_f={q:w for q in noun_map.keys() for w in noun_map_dist}
    try:
        return noun_f
    except:
        return noun_map
    finally:
        print(f"done: elapsed in {t()-t0:.4f}s")

def make_wcld(f_noun,output_imgfile=output_imgfile,font=font,
    mask=None,size=(1920,1080),img=False):
    t0=t()
    mask=None#np.array(Image.open("image.png")
    wc=WordCloud(font_path=font,
        height=size[0],width=size[1],
        mask=mask,normalize_plurals=False,
        max_words=10000)
    wc=wc.fit_words(f_noun)
    if img:
        wc.to_file(output_imgfile)
    plt.imshow(wc,interpolation="lanczos")
    plt.axis("off")
    print(f"done: elasped in {t()-t0:.4f}s")
    plt.show()

make_wcld(noun_freq(get_txt("ko.txt"),n_noun=50,norm=True),img=True)

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
    cursor.vocabulary_.get("정신분열증")