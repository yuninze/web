import numpy.random as nprnd
import matplotlib.pyplot as plt
from time import time as t
from collections import Counter
from wordcloud import WordCloud
from konlpy.tag import Okt

jvm="C:/Program Files/Java/jdk-18/bin/server/jvm.dll"
font="C:/code/basic/GBR.ttf"
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

def noun_freq(text,l_noun=2,n_noun=500,mtl=2.71)->dict:
    t0=t()
    okt=Okt(jvmpath=jvm)
    noun=okt.nouns(text)
    #l_noun specifies len of noun
    noun=Counter([q for q in noun if len(q)>=l_noun])
    f_noun={q:int(w*mtl) for q,w in noun.most_common(n_noun)}
    print(f"done: elapsed in {t()-t0:.4f}s")
    return f_noun

def make_wcld(f_noun,output_imgfile=output_imgfile,font=font,
    mask=None,size=(1920,1080),norm=False,img=False):
    t0=t()
    mask=None#np.array(Image.open("image.png")
    wc=WordCloud(font_path=font,
        height=size[0],width=size[1],
        mask=mask,normalize_plurals=norm,
        max_words=10000)
    wc=wc.fit_words(f_noun)
    if img:
        wc.to_file(output_imgfile)
    plt.imshow(wc,interpolation="lanczos")
    plt.axis("off")
    print(f"done: elasped in {t()-t0:.4f}s")
    plt.show()

make_wcld(noun_freq(get_txt("ko.txt"),n_noun=200,mtl=3),img=True)

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