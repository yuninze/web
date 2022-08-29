import requests as rqst
from random import random
from time import sleep

ua={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "\
    "AppleWebKit/537.36 (KHTML, like Gecko) "\
    "Chrome/104.0.0.0 Safari/537.36"}

def dia():
    urlprefix="http://classic.battle.net/supersecrest/"

    with open("w_dia",encoding="utf-8-sig") as listfile:
        urls=(listfile.read()).split(sep="\n\n")

    while not urls==[]:
        for url in urls:
            sleep(random())
            qfilename=url.replace(f"{urlprefix}","")
            try:
                q=rqst.get(
                url=url,
                verify=False,
                timeout=30,
                headers={"user-agent":ua})
                if q.status_code==200:
                    with open(qfilename,"wb") as qfile:
                        qfile.write(q.content)
                        urls.remove(url)
                        print(f"{url}: success")
                else:
                    print(f"{url}: {q.status_code}")
            except:
                print(f"{url}: failed")
                continue

    print(f"done")