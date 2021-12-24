import os
import pandas as pd

os.chdir("c:\\")
test=pd.read_csv("testtest.csv",encoding="utf-8-sig")

test["isdupe"]=None
test.apply(lambda c:str(c))

test["slave"]="참여"
test["slaveName"]="크라우드웍스"
test["ingunbi"]="일용임금(크라우드소싱)"
test[16]="X"

for z in test.index:
    try:
        if test.loc[z,"nationality"]=="대한민국":
            test.loc[z,"isForeign"]="내국인"
        elif test.loc[z,"nationality"]=="nan":
            test.loc[z,"isForeign"]="입력거부"
        elif test.loc[z,"nationality"]==None:
            test.loc[z,"isForeign"]="입력거부"
    except:
        test.loc[z,"isForeign"]="입력거부"
    try:
        if test.loc[z,"citizenNumber"][7]=="1":
            test.loc[z,"sex"]="남자"
        elif test.loc[z,"citizenNumber"][7]=="2":
            test.loc[z,"sex"]="여자"
    except:
        try:
            if len(test.loc[z,"citizenNumber"])<7:
                test.loc[z,"sex"]="입력거부"
            elif test.loc[z,"citizenNumber"]=="nan":
                test.loc[z,"sex"]="입력거부"
                test.loc[z,"citizenNumber"]="입력거부"
            else:
                test.loc[z,"citizenNumber"]="입력거부"
                test.loc[z,"sex"]="입력거부"
        except:
            test.loc[z,"citizenNumber"]="입력거부"
            test.loc[z,"sex"]="입력거부"
    if len(test.loc[z,"citizenNumber"])>7:
        try:
            a=int(test.loc[z,"citizenNumber"][:2])
            if a<21:
                b=21-a
            else:
                b=a-21
            test.loc[z,"userAge"]=b
        except:
            test.loc[z,"userAge"]="입력거부"
    try:
        if test.loc[z,"userAge"]<34:
            test.loc[z,"young"]="O"
        else:
            test.loc[z,"young"]="X"
    except:
        test.loc[z,"young"]="unknown"
    try:
        a=int(test.loc[z,"userAge"])-0
        if a<10:
            test.loc[z,"ageRange"]="0대"
        elif a<20:
            test.loc[z,"ageRange"]="10대"
        elif a<30:
            test.loc[z,"ageRange"]="20대"
        elif a<40:
            test.loc[z,"ageRange"]="30대"
        elif a<50:
            test.loc[z,"ageRange"]="40대"
        elif a<60:
            test.loc[z,"ageRange"]="50대"
        elif a<70:
            test.loc[z,"ageRange"]="60대"
        elif a<80:
            test.loc[z,"ageRange"]="70대"
        elif a<90:
            test.loc[z,"ageRange"]="80대"
        elif a<100:
            test.loc[z,"ageRange"]="90대"
        elif a<110:
            test.loc[z,"ageRange"]="100대"
        else:
            test.loc[z,"ageRange"]="100대 이상"
    except:
        test.loc[z,"ageRange"]="계산실패"
    
    test.loc[z,"concat"]=str(test.loc[z,"guazeNum"])+str(test.loc[z,"slaveName"])+str(z)+str(test.loc[z,"citizenNumber"])
            





test.to_csv("test0.csv",encoding="utf-8-sig",index=False)