import os
import requests
import threading
import concurrent.futures
from bs4 import BeautifulSoup as bs

ua={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "\
    "AppleWebKit/537.36 (KHTML, like Gecko) "\
    "Chrome/104.0.0.0 Safari/537.36"}

def dn(v):
    #(vidname,vidurl)
    os.system(f'''
        ffmpeg -loglevel 32 -i "{v[1]}" \
        -bsf:a aac_adtstoasc -c copy "C:/0/{v[0]}.mp4"''')

def visit(url,idx):
    url=url
    try:
        #if fail return None
        w=bs(
            requests.get(
                url=f"{url}{idx}",
                headers=ua).text)
        #if fail return None
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
        thread=threading.Thread(target=visit,args=[y])
        thread.daemon=True
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

def exec(url,mx,mn,max_workers=50):
    #canvas for each results the callable
    rtn=[]
    #with with statement shutdown method is not needed
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers) as t:
        #submit future objects: 
        works={t.submit(visit,url,q):q for q in range(mx,mn,-1)}
        #result collection: as_completed
        for work in concurrent.futures.as_completed(works):
            #get index by future object
            q=works[work]
            #yielded result from the callable per future object
            rslt=work.result()
            if rslt is None:
                print(f"exception: {url}{q}")
                t.shutdown(wait=True,
                cancel_futures=True)
            elif rslt is False:
                rtn.append(q)
                print(f"failed: {q}")
            else:
                print(f"got: {q}")
    return rtn