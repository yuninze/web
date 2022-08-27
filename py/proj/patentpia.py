import pandas as pd

encoding="utf-8-sig"

def lighting_text(
        src:str="patentpia.xlsx",
        colBasis:tuple=('no.'
            'KW_EN',
            'KW_KO',
            'SENTENCE_EN',
            'SENTENCE_KO'))->pd.DataFrame:
    '''patentPia'''
    pp=pd.read_excel(src)
    #check as patentpia
    if tuple(pp.columns)==colBasis:
        incIdxLen=pp.index.nunique()
        pp=pp.set_index("no.")
        if incIdxLen==pp.index.nunique():
            #check whether engWord in engSent
            engWordNotInEngSent={"word":[]}
            for q in pp.index:
                engWord=pp.loc[q,"KW_EN"]
                engSent=pp.loc[q,"SENTENCE_EN"]
                if not engWord in engSent:
                    engWordNotInEngSent["word"].append(engWord)
            engWordNotInEngSentCnt=len(engWordNotInEngSent["word"])
            print(f"{engWordNotInEngSentCnt=}")
            if engWordNotInEngSentCnt==0:
                #main execution block: highlighting
                for q in enumerate(pp.index):
                    engWord=pp.loc[q[1],"KW_EN"]
                    pp.loc[q[1],"SENTENCE_EN"]=(
                    pp.loc[q[1],"SENTENCE_EN"]
                    .replace(engWord,
                        f'''<span style="
                        font-weight:bold;
                        color:#FE0000">{engWord}</span>'''))
                pp.to_csv("patentpia.csv",encoding=encoding)
                return None
            raise NameError("unmatching word in the content")
        raise IndexError("dupe in no. column")
    raise NameError("peculiar content")