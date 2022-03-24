import pandas as pd

encoding="utf-8-sig"

def lighting_text(
        srcData:str="patentpia.xlsx",
        colBasis:tuple=('no.'
            'KW_EN',
            'KW_KO',
            'SENTENCE_EN',
            'SENTENCE_KO')
        )->pd.DataFrame:
    '''tag'''
    pp=pd.read_excel(srcData)
    #check as patentpia
    if not tuple(pp.columns)==colBasis:
        raise NameError("column name, sequence does not match")
    incIdxLen=pp.index.nunique()
    pp=pp.set_index("no.")
    if incIdxLen!=pp.index.nunique():
        raise IndexError("duplicated value exist in no. column")
    #check whether engWord in engSent
    engWordNotInEngSent={"word":[]}
    for q in pp.index:
        engWord=pp.loc[q,"KW_EN"]
        engSent=pp.loc[q,"SENTENCE_EN"]
        if not engWord in engSent:
            engWordNotInEngSent["word"].append(engWord)
    print(str(len(engWordNotInEngSent["word"])))
    #main excution block: highlighting
    for q in enumerate(pp.index):
        engWord=pp.loc[q[1],"KW_EN"]
        pp.loc[q[1],"SENTENCE_EN"]=(pp.loc[q[1],"SENTENCE_EN"]
        .replace(engWord,
            f'''<span style="font-weight:bold;color:#FE0000">{engWord}</span>'''))
    pp.to_csv("patentpia.csv",encoding=encoding)
    return pp