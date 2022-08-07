import requests
from random import random
from time import sleep

ua="py-yuninze-downdiablo2mp3"
urlprefix="http://classic.battle.net/supersecrest/"

with open("dia.txt",encoding="utf-8-sig") as listfile:
    urls=(listfile.read()).split(sep="\n\n")

while not urls==[]:
    for url in urls:
        secs=(random()+1)*5,sleep(secs)
        qfilename=url.replace(f"{urlprefix}","")
        try:
            q=requests.get(
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