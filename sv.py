import os
import csv
import requests
import threading
import concurrent.futures
import numpy as np
from time import time
from bs4 import BeautifulSoup as bs

ua={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "\
    "AppleWebKit/537.36 (KHTML, like Gecko) "\
    "Chrome/104.0.0.0 Safari/537.36"}

def dn(v):
    # (vidname,vidurl)
    os.system(
        f'ffmpeg -n -loglevel 24 '
        f'-i "{v[1]}" '
        f'-user_agent "{ua["user-agent"]}" ' 
        f'-multiple_requests 0 -reconnect_at_eof 1 ' 
        f'-reconnect_streamed 1 -reconnect_on_network_error 1 ' 
        f'-bsf:a aac_adtstoasc -c copy '
        f'"d:/rslt/{v[2]}_{v[0]}.mp4"')

def visit(url,idx):
    url=f"{url}{idx}"
    try:
        w=bs(requests.get(url,headers=ua).text)
        e=requests.get(w.iframe["src"],headers=ua)
        if not e.status_code==200:
            return False,url,f"{e.status_code}"
        e=bs(e.text)
        vidname=e.select("meta")[ 6]["content"]
        vidurl =e.select("meta")[17]["content"]
        dn((vidname,vidurl,idx))
        return True,f"{idx}_{vidname}.mp4"
    except Exception as ng:
        return False,url,ng

def exec(url,mx,mn,max_workers=200):
    t0=time()
    oks,ngs=[],[]
    #with with statement shutdown method is not needed
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers) as te:
        #submit future objects
        works={te.submit(visit,url,q):q for q in np.arange(mn,mx,1)}
        #result collection: as_completed
        for work in concurrent.futures.as_completed(works):
            #get index by future
            q=works[work]
            #yielded result from the callable per future
            try:
                rslt=work.result(timeout=2048)
            except TimeoutError as ng:
                #idx+reason
                ngs.append((q,ng))
                te.shutdown(wait=True,cancel_futures=False)
            else:
                if rslt[0] is True:
                    oks.append(rslt[1])
                    print(f"ok: {q}")
                elif rslt[0] is False:
                    #idx+reason
                    ngs.append((rslt[1],rslt[2]))
                    print(f"ng: {q} ({rslt[2]})")
    with open("d:/rslt.csv","w",encoding="utf-8",newline="") as csvfile:
        (csv.writer(csvfile)).writerows(ngs)
    print(f"completed in {time()-t0:.2f}s")
    return oks,ngs

def sanitize(oks=None,path="d:/rslt/"):
    q=[q.name for q in os.scandir(path) 
        if q.is_file and q.name.endswith(".mp4") and q.stat().st_size==0]
    print(f"zero-sized files: {len(q)}")
    for filename in q:
        os.remove(path+filename)
    if not oks is None:
        q=list(set([q.name for q in os.scandir(path) 
            if q.is_file and q.name.endswith(".mp4")])-set(oks))
        for filename in q:
            os.remove(path+filename)
        return q

def mt(mx,mn):
    threads=[]
    for y in range(mx,mn,-1):
        thread=threading.Thread(target=visit,args=[y])
        thread.daemon=True
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

def prof(q):
    import cProfile
    import pstats
    with cProfile.Profile() as p:
        exec(q[0],q[1],q[2])
    stats=pstats.Stats(p)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()