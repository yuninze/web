import os,glob,shutil;import numpy as np;
import cv2
from PIL import Image
os.chdir("Z:\\FRIEND\\yun_work\\code\\cv2")

def sani(a):
    if isinstance(a,str):
        return a.lower().strip()
    if isinstance(a,(int,float)):
        return np.uint8(a)
    else:
        return a

def file(p):
    os.chdir(sani(p))
    a=glob.glob("*.jp*")
    if len(a)<=0:
        print("none")
    il=[]
    for x in range(len(a)):
        i=dict()
        i[str(a[x])]=cv2.imread(a[x])
        il[len(il):]=[i]
    return il

def rs(path,d,ratio,quant):
    if "\\" not in path:
        path=str(path).replace("\\","\\\\")
    os.chdir(path)
    if d is not None:
        if os.path.isdir(d):
            shutil.rmtree(d)
            print("..deleted")
        else:
            os.mkdir(d)
    if ratio<1:
        ratio=float(ratio)
    elif ratio>1:
        ratio=float(ratio*0.01)
    elif ratio==1:
        ratio=int(ratio)
    if quant<=100:
        quant=int(quant)
    elif quant>=100:
        quant=100
    f=glob.glob("*.jp*")
    for x in f:
        if os.path.getsize(x)==0:
            f.remove(x)
    for x in f:
        img=(Image.open(str(x),"r")).convert("RGB")
        imgx,imgy=(int(img.size[a]*ratio) for a in [0,1])
        imgfile=img.resize((imgx,imgy),Image.LANCZOS)
        if d is None:
            imgfile.save(str(x),"JPEG",quality=int(quant),progressive=True,optimize=True)
        else:
            imgfile.save(d+"//"+str(x),"JPEG",quality=int(quant),progressive=True,optimize=True)
        print(str(x)+"..: "+str(imgx)+" x "+str(imgy))
    print("..done")
    return None
#rs("D:\\atc\\total",None,1,20)

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
#show("a.jpg")

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
    os.chdir(path)
    if len(glob.glob("*.jp*"))==0:
        raise OSError("")
    else:
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

def stamp(fgifile,bgipath):
    os.chdir(bgipath)
    #load foreground imagefile as a foreground image
    with Image.open(fgifile) as fgi:
        #resize if bgi is large
        if sum(fgi.size)>800:
            #pngfile is not supported as 
            if fgi.filename.endswith('.png'):
                pass
            else:
                fgi=fgi.resize(([np.uint16(x*0.7) for x in fgi.size]),Image.LANCZOS)
                print(f'resized: {fgi.size[0]} x {fgi.size[1]}')
        else:
            print(f'not resized: {fgi.size[0]} x {fgi.size[1]}')
        #get bgifilenamelist form the bgipath
        bgifile=glob.glob('*.jp*')
        for bgi in bgifile:
            factor=np.random.random_sample(2)*2
            #load background imagefile as a background image
            with Image.open(bgi,'r') as bgi:
                #preserve bgi filename
                bgifilename=bgi.filename
                #channelConvert RGBA
                bgi=bgi.convert('RGBA')
                #have initial coordinates
                bgix0,bgiy0=bgi.size
                #have coordinates of upper-left region
                bgix1,bgiy1=np.uint16(bgix0*0.1),np.uint16(bgiy0*0.05)
                #have moderately moved coordinates of upper-left region
                bgix2,bgiy2=tuple(np.uint16(w) for w in (bgix1*factor[0],bgiy1*factor[1]))
                print(str(bgix2),str(bgiy2))
                #paste fgi to bgi
                bgi.paste(fgi,box=(bgix1+bgix2,bgiy1+bgiy2),mask=fgi.convert('RGBA'))
                #channelConvert RGB
                bgi=bgi.convert('RGB')
                #save bgi to bgiimagefile
                bgi.save('z'+bgifilename,'JPEG',quality=40,progressive=True,optimize=True)