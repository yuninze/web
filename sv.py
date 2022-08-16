from asyncio import as_completed
import os
import requests
import threading
import concurrent.futures
from bs4 import BeautifulSoup as bs

ua={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "\
    "AppleWebKit/537.36 (KHTML, like Gecko) "\
    "Chrome/104.0.0.0 Safari/537.36"}
fails=[]

def dn(v):
    #(vidname,vidurl)
    os.system(f'''
        ffmpeg -loglevel 32 -i "{v[1]}" \
        -bsf:a aac_adtstoasc -c copy "C:/0/{v[0]}.mp4"''')

def visit(param):
    #(url,mx,mn,dic)
    vid={}
    for q in range(param[1],param[2],-1):
        try:
            w=bs(
                requests.get(
                    url=f"{param[0]}{q}",
                    headers=ua).text)
            e=bs(
                requests.get(
                    url=w.iframe["src"],
                    headers=ua).text)
            vidname=e.select("meta")[ 6]["content"]
            vidurl =e.select("meta")[17]["content"]
            dn((vidname,vidurl))
        except:
            print(f"x: {q}")
    if param[3]:
        return vid

def visita(url,idx):
    url=url
    try:
        w=bs(
            requests.get(
                url=f"{url}{idx}",
                headers=ua).text)
        e=bs(
            requests.get(
                url=w.iframe["src"],
                headers=ua).text)
        vidname=e.select("meta")[ 6]["content"]
        vidurl =e.select("meta")[17]["content"]
        #dn((vidname,vidurl))
        return True
    except:
        return False

def mt(mx,mn):
    threads=[]
    for y in range(mx,mn,-1):
        thread=threading.Thread(target=visita,args=[y])
        thread.daemon=True
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

def exec(url,mx,mn,max_workers=50):
    #canvas for each results of threads
    rtn={}
    #with with statement shutdown method is not needed
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers) as t:
        #specifies each threads by the indices
        works={t.submit(visita,url,q):q for q in range(mx,mn,-1)}
        #result collection: as_completed
        for work in concurrent.futures.as_completed(works):
            #assign thread
            q=works[work]
            #yielded result from the callable, per thread
            rslt=work.result()
            #saving result per index
            rtn[q]=rslt
            if rslt is False:
                print(f"failed: {q}")
            else:
                print(f"got: {q}")
    return rtn