import webbrowser
import numpy.random as nprnd
from collections import Counter
from konlpy.tag import Okt

jvmpath="C:/Program Files/Java/jdk-18/bin/server/jvm.dll"
font=fontfile="c:/code/IBMPlexSansKR.ttf"
text=""

filename="wc.png"

def gdstrb()->tuple:
    return tuple(nprnd.default_rng().integers(0,255,size=3))

def parsing_nn(
    text_data=text,
    l_noun=2,
    n_noun=25,
    coe=10)->dict:
    okt=Okt(jvmpath=jvmpath)
    noun=okt.nouns(text_data)
    noun=[q for q in noun if len(q)>=l_noun]
    n_nouns=Counter(noun)
    return [{"color":gdstrb(),"tag":q,"size":w*coe}
        for q,w in n_nouns.most_common(n_noun)]

def draw_wc(tags,filename=filename,fontname=fontname,):
    pytagcloud.create_tag_image(tags,filename,fontname=fontname,size=(1024,768))
    webbrowser.open_new_tab(filename)
    return None

def read_doc():
    filename=input(f"filename: ")
    if filename:
        with open(filename,encoding="utf-8") as file:
            return file.read()

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