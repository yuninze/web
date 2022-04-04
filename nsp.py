import numpy.random as nprnd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import time as t
from collections import Counter
from seaborn import diverging_palette
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

def l2_scaler(i,l):
    i=np.array(i,dtype=np.float64)
    base=i.prod()**(1/l)
    dist=np.sqrt((i-base)**2)
    return dist

def noun_freq(text,
    l_noun=2,
    n_noun=500,
    norm=True)->dict:
    t0=t()
    okt=Okt(jvmpath=jvm)
    noun=okt.nouns(text)
    noun=Counter([q for q in noun if len(q)>=l_noun])
    noun_map={q:w for q,w in noun.most_common(n_noun)}
    if norm:
        noun_map_len=len(noun)
        noun_map_base=[noun_map[q] for q in noun_map.keys()]
        noun_map_dist=l2_scaler(noun_map_base,noun_map_len)
        noun_f={q:w for q,w in zip(noun_map.keys(),noun_map_dist)}
    try:
        return noun_f
    except:
        return noun_map
    finally:
        print(f"noun_freq: elapsed in {t()-t0:.4f}s")

def quick_visual(occur_data):
    t0=t()
    data=pd.DataFrame.from_dict(occur_data,
        orient="index",
        columns=["occurance"])
    data.plot.bar(rot=45)
    plt.figure(figsize=(100,50))
    plt.xlabel("noun_name")
    plt.ylabel("noun_freq")
    print(f"quick_visual: elapsed in {t()-t0:.4f}s")
    plt.show()

def make_wcld(f_noun,
    wc_font=font,
    wc_size=(1000,1000),
    wc_mask=None,wc_oval_shape=True,
    wc_cmap=diverging_palette(240,10,as_cmap=True),
    wc_bgcolor=None,
    wc_output_imgfile=output_imgfile,
    wc_output_imgfile_mode="RGBA",
    show=False):
    t0=t()
    if wc_oval_shape:
        x,y=np.ogrid[:wc_size[0],:wc_size[1]]
        wc_mask=(
                (x//2)**2 + (y//2)**2 > 
                ((sum(wc_size)//2)-(sum(wc_size)*0.25))**2
				)
        #bool to int
        wc_mask=wc_mask.astype(int)*255
    wc=WordCloud(max_words=1000,
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
n_freq=noun_freq(txt,n_noun=100,norm=True)
make_wcld(n_freq,
    wc_bgcolor="black",
    wc_output_imgfile_mode="RGB",
    show=True)

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