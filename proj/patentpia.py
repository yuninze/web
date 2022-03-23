import pandas as pd

encoding="utf-8-sig"

def lighting_text(srcData:str="patentpia.xlsx")->pd.DataFrame:
    '''r'''
    pp=pd.read_excel(srcData)
    #check as patentpia
    ppOrgColName=(
        'no.'
        'KW_EN',
        'KW_KO_기계번역',
        'SENTENCE_EN',
        'SENTENCE_KO_기계번역')
    for q in pp.columns:
        if not q in ppOrgColName:
            raise NameError(f"column name does not match: {q}")
    incIdxLen=pp.index.nunique()
    pp=pp.set_index("no.")
    if incIdxLen!=pp.index.nunique():
        raise IndexError("duplicated value exist in no. column")
    if pp.shape[1]!=4:
        raise IndexError(f"column numbers should be 4, input is {pp.shape[1]}")
    #check whether engWord in engSent
    engWordNotInEngSent={"word":[]}
    for q in pp.index:
        engWord=pp.loc[q,"KW_EN"]
        engSent=pp.loc[q,"SENTENCE_EN"]
        if not engWord in engSent:
            engWordNotInEngSent["word"].append(engWord)
    print(str(len(engWordNotInEngSent["word"])))
    #highlighting tag insertion
    for q in enumerate(pp.index):
        engWord=pp.loc[q[1],"KW_EN"]
        pp.loc[q[1],"SENTENCE_EN"]=(pp.loc[q[1],"SENTENCE_EN"]
        .replace(engWord,'''<span style="font-weight:bold;color:#FE0000">engVal</span>'''))
    pp.to_csv("patentpia.csv",encoding=encoding)
    return pp