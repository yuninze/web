def ta0(fileObjectName):
    """
    Based on complicated multi-indexes,
    convert columns into per-index stacked rows.
    converted per-index stacked rows would be
    a new component of multi-indexes.
    """
    df=pd.read_csv(fileObjectName,encoding=enc).reset_index()
    colnum=len(df.columns)
    try:
        df.set_index(["pid","mail","name"],inplace=False)
    except:
        assert NotImplementedError("Multi-index element not percieved")
    if colnum==4:
        df["count0t"]=df.groupby(["pid","mail","name"])["count0"].transform("sum")
    elif colnum==5:
        df["count0t"]=df.groupby(["pid","mail","name"])["count0"].transform("sum")
        df["count1t"]=df.groupby(["pid","mail","name"])["count1"].transform("sum")
    else:
        assert IndexError("FileObject is irrelevant to DETA")
    return df.set_index(["pid","mail","name"]).stack(dropna=True)

for x in f.index:
    row=f.loc[x,"variety"]
    if "장애" in row:
        f.loc[x,"zangae"]="O"
    elif "임신" in row:
        f.loc[x,"preg"]="O"
    elif "단절" in row:
        f.loc[x,"gzy"]="O"
    elif "보훈" in row:
        f.loc[x,"bohun"]="O"
    elif "다문화" in row:
        f.loc[x,"damunwha"]="O"
    elif "초등" in row:
        f.loc[x,"choding"]="O"
    elif "대학생" in row:
        f.loc[x,"daeding"]="O"
    elif "투잡" in row:
        f.loc[x,"jobtwo"]="O"
    elif "미취업자" in row:
        f.loc[x,"jobno"]="O"
    elif "실직자" in row:
        f.loc[x,"jobloss"]="O"
    elif "저소득" in row:
        f.loc[x,"lowincome"]="O"
    elif "장기실업" in row:
        f.loc[x,"jobless"]="O"
    elif "가장" in row:
        f.loc[x,"mobuzang"]="O"
    elif "이주" in row:
        f.loc[x,"visamarry"]="O"
    elif "북한" in row:
        f.loc[x,"bukhan"]="O"
    elif "자영업" in row:
        f.loc[x,"selfempoly"]="O"
    elif "AI" in row:
        f.loc[x,"aihub"]="O"
    else:
        pass

