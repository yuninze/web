import os
import time
import requests
import cv2
import pandas as pd
import numpy as np
from io import BytesIO
from PIL import Image

def img_from_df():
    srcpath=input("srcpath: ")
    if not srcpath:
        srcpath="C:/Users/yinze/Downloads/kiwi/kiwi_src.csv"
    src=pd.read_csv(srcpath)
    srccol=input("srccol: ")
    if not srccol:
        srccol="rep_image_path"
    srcprefix=input("srcprefix: ")
    t0=time()
    for q in src.loc[:,srccol]:
        iurl=srcprefix+q
        iu=requests.get(iurl)
        #https://docs.python-requests.org/en/latest/user/quickstart/#response-status-codes
        if iu.status_code==200:
            print(f"ok: {iu.status_code}->{q}")
            with Image.open(BytesIO(iu.content)) as ib:
                ifname=q.replace(".png","jpg")
                ib=ib.convert("RGB")
                ib.save(f"{ifname}",
                    "JPEG",
                    quality=10,
                    progressive=True,
                    optimize=True)
        else:
            print(f"err: {iu.status_code}->{q}")
    return print(f"done with {len(src)} images, elapsed {time()-t0}s")
    
def stamp(fgifile,bgipath,ts=130,ss=200,rnd=2,qual=5):
    #check object size
    if ts>120:
        bgifile=[bgipath+'/'+x for x in os.listdir(bgipath) if '.jp' in x]
        for bgifile in bgifile:
            with Image.open(bgifile) as bgi:
                with Image.open(fgifile) as fgi:
                    #if pngfile check imagemode
                    if fgi.filename.endswith('.png'):
                        ispng=True
                        if not fgi.mode=='RGBA':
                            raise ValueError(f'peculiar pngfile ({fgi.mode=})')
                    #initiate f, locf, sizef
                    seed=np.random.random_sample(10)
                    f=np.random.choice(seed,size=2)
                    lf=f*rnd
                    sf=f[0]*ss
                    #have ar
                    ar=fgi.size[0]/fgi.size[1]
                    #have mod
                    mod=(fgi.size[0]/ts,
                        fgi.size[1]/ts)
                    adi=(sf*ar,sf)
                    size=tuple(
                        np.uint16(x) for x in [(
                        fgi.size[0]/mod[0])*ar+adi[0],
                        fgi.size[1]/mod[1]+adi[1]])
                    #resize if bgi is large
                    if sum(fgi.size)>500:
                        print(f'resizing: {fgi.filename}: {size[0]} x {size[1]}')
                        fgi=fgi.resize(size,Image.LANCZOS)
                    else:
                        print(f'not resized: {fgi.filename}: {fgi.size[0]} x {fgi.size[1]}')
                    #preserve bgi filename
                    bgifilename=bgi.filename
                    #channelConvert RGBA
                    bgi=bgi.convert('RGBA')
                    #have initial coordinates
                    bgix0,bgiy0=bgi.size
                    #have coordinates of upper-left region
                    bgix1,bgiy1=np.uint16(bgix0*0.05),np.uint16(bgiy0*0.05)
                    #have moderately moved coordinates of upper-left region
                    bgix2,bgiy2=tuple(
                        np.uint16(w) for w in (
                        bgix1*lf[0]+(lf[0]*100),
                        bgiy1*lf[1]+(lf[1]*100)))
                    #paste fgi to bgi
                    bgi.paste(fgi,
                        box=(bgix1+bgix2,bgiy1+bgiy2),
                        mask=fgi.convert('RGBA'))
                    #channelConvert RGB
                    bgi=bgi.convert('RGB')
                    #save bgi to bgiimagefile
                    bgifilename=bgifilename[(bgifilename.rfind('/')+1):]
                    bgi.save('x'+bgifilename,
                        'JPEG',
                        quality=qual,
                        progressive=True,
                        optimize=True)
                return None
    raise ValueError('object size is peculiar')

def rs(path:str,
        ratio:int,
        quant:int=10)->None:
    ratio=ratio*0.01
    if not quant<=100:
        quant=100
    if not path.endswith("//"):
        path=f"{path}//"
    os.chdir(path)
    imgfile=[q.name for q in os.scandir() 
            if q.name.endswith(".jpg") and q.stat().st_size!=0]
    for q in imgfile:
        with Image.open(q) as ib:
            ibx,iby=int(ib.size[q]*ratio)
            ib=(ib
                .resize((ibx,iby),Image.LANCZOS)
                .convert("RGB"))
            ib.save(f"{path}rs_{q}",
                "JPEG",
                quality=quant,
                progressive=True,
                optimize=True)
            print(f"{q}: {ibx} x {iby}")
    print(f"SUCCESS: {len(imgfile)} with files")
    return None

#debt
def show(i):
    if isinstance(i,str):
        a=i
        cv2.imshow("img",cv2.imread(i))
        cv2.waitKey(0),cv2.destroyAllWindows()
        return print(str(a))
    elif isinstance(i,list):
        try:
            for x in range(len(i)):
                cv2.imshow("img",cv2.imread(i[x]))
                cv2.waitkey(0),cv2.destoryAllWindows()
                return print(str(len(i)))
        except:
            if len(i) is False:
                raise TypeError("input was False")
            elif r"*.jp*" in str(i[0]):
                a=len(i)
                for x in range(a+1):
                    cv2.imshow("img",cv2.imread(x))
                    cv2.waitKey(0),cv2.destroyAllWindows()
                return print(str(a))
            elif isinstance(i,np.ndarray):
                a=i.shape
                for x in range(len(i)):
                    cv2.imshow("img",x)
                    cv2.waitKey(0),cv2.destroyAllWindows()
                return print(str(a))
            else:
                raise TypeError("")
    elif isinstance(i,dict):
        a=len(i)
        b,c=list(i),list(i.values())
        for x in b:
            cv2.imshow(str(b[x]),c[x])
            cv2.waitKey(0),cv2.destroyAllWindows()
        return print(str(a))

def bloc(blockNumber,quant=30):
    if blockNumber>=6:
        blockNumber=6
    else:
        blockNumber=int(blockNumber)
    if type(quant)==str:
        raise TypeError("quant")
    elif quant<=100:
        quant=int(quant)
    else:
        quant=50
    workplace=glob.glob("*.jp*")
    print(str(os.getcwd())+": "+str(workplace))
    for x in workplace:
        img0=cv2.imread(x,0)
        yl,xl=len(img0[0]),len(img0[1])
        if yl<xl:
            yr,xr=int(0.9*yl),int(0.8*xl)
        elif yl>xl:
            yr,xr=int(0.8*yl),int(0.9*xl)
        elif yl==xl:
            yr,xr=int(0.8*yl),int(0.8*xl)
        img0=img0[yr:yl-yr,xr:xl-xr]
        try:
            img0y0,img0x0,img0z0=img0.shape
        except:
            img0y0,img0x0,img0z0=img0.shape[0],img0.shape[1],None
        img0yCoe,img0xCoe=((i//blockNumber,i%blockNumber) for i in (img0y0,img0x0))
        img0y1,img0x1=((i//blockNumber) for i in (img0y0-img0yCoe[1],img0x0-img0xCoe[1]))
        block=[]
        for y in range(blockNumber):
            for x in range(blockNumber):
                block[len(block):]=[img0[y*img0y1:y*img0y1+img0y1,x*img0x1:x*img0x1+img0x1]]
        cv2.imshow("block",block[0])
        ###norm
        n0=[]
        n1=block//quant
        print("...block.shape: "+str(block.shape))
        print("...n1.shape: "+str(n1.shape))
        for n in range(len(n1)):
            n2=dict()
            n2[n]=int(sum([block[x] for x in range(quant)]))//quant
            n0.extend(n2)
        print(n0)
    return None
bloc(3,3)

def face(path):
    for z in glob.glob("*.jp*"):
        ib=cv2.imread(z)
        c=cv2.CascadeClassifier("frontalFace.xml").detectMultiScale(ib)
        for b in range(len(c)):
            x,y,w,h=c[b]
            x2,y2=x+w,y+h
            cv2.rectangle(ib,(x,y),(x2,y2),(0,0,255),4)
            cv2.imshow(str(x),ib)
            cv2.waitKey(0),cv2.destroyAllWindows()
    return None

def data(a):
    a=str(a+".json")
    b=json.load(open(a,"r",encoding="utf-8-sig"))
    c=[]
    for x in range(len(b["result"])):
        d=dict()
        c["id"]=b["result"][x]["dataID"]
        c["imagefile"]=b["result"][x]["gp_trash_bb"]["sourceValue"]
        c["x0"]=b["result"][x]["gp_trash_bb"]["data"][0]["value"]["coords"]["tl"]["x"]
        c["y0"]=b["result"][x]["gp_trash_bb"]["data"][0]["value"]["coords"]["tl"]["y"]
        c["x1"]=b["result"][x]["gp_trash_bb"]["data"][0]["value"]["coords"]["bl"]["x"]
        c["y1"]=b["result"][x]["gp_trash_bb"]["data"][0]["value"]["coords"]["bl"]["y"]
    return None