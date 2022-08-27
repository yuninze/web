import csv
import sqlite3
import pandas as pd

class db:
    '''
    Sequential todo element block containing 
    sequential methods to load df/fileObj to db/sqlite
    '''
    #db.type
    def type(filename:str)->int:
        if filename.endswith(".csv"):
            return 0
        elif filename.endswith((".xlsx",".xls")):
            return 1

    #db.to_db
    def from_df(db:str="c:/code/db.db",
            chk:bool=True,
            use:bool=False):
        #get a connect object, cursor object
        con=sqlite3.connect(f"{db}")
        cur=con.cursor()
        #get a df
        while True:
            filename=input("dbpath: ")
            if not filename:
                break
            else:
                filetype=type(filename)
            if filetype==0:
                df=pd.read_csv(filename)
            elif filetype==1:
                df=pd.read_excel(filename)
            print(f"loaded: {filename} {df.shape}")
            #get a tablename, insert into db
            tablename=input("tablename: ")
            df.to_sql(tablename,
                con=con,
                if_exists="replace",
                index_label=f"idx_{tablename}")
            if chk:
                *(map(print,{q[1][1] for q in enumerate
                (cur.execute(f'select * from {tablename}'))
                })),
            print(f"success: {filename} -> {db} -> {tablename}")
        if use:
            return cur
        else:
            con.close() #pd.to_sql automatically commits
            return None

    def queryexec(cur,
            query:str)->tuple:
        '''
        '''
        try:
            return cur.execute(query),1
        except (sqlite3.ProgrammingError,
                sqlite3.OperationalError,
                sqlite3.NotSupportedError) as e:
            return print(f"->{e} '{query}'"),2

    def query()->None:
        note={"true":[],"false":[]}
        danger=("update","delete")
        agree=("y","yes","ok")
        dbname=input("db: ")
        if not dbname:
            dbname="c:/code/db.db"
        with sqlite3.connect(dbname) as con:
            cur=con.cursor()
            print(f"connected: {dbname}")
            while dbname:
                query=input(f"{dbname}->")
                #quit while status by False query
                if not query:
                    cur.close()
                    break
                #history feature
                if query=="history":
                    for q in enumerate(note["true"]):
                        print(f"{q[0]}: {q[1]}")
                    continue
                #filter for select, pragma
                if any(map(query.__contains__,("select","pragma"))):
                    queryresult=db.queryexec(cur,query)
                    if not queryresult[1]==1:
                        note["false"].append(query)
                        continue
                    note["true"].append(query)
                    selectresult=queryresult[0].fetchall()
                    selectrows=len(selectresult)
                    if selectrows>49:
                        for q in selectresult[:49]:
                            print(q)
                        print(f"->remaining rows: {selectrows-49}")
                    else:
                        for q in selectresult:
                            print(q)
                        print(f"->rows: {selectrows}")
                    continue
                #filter for update, delete
                if any(map(query.__contains__,danger)):
                        if not "where" in query:
                            warn=input("->no where clause ")
                            if not any(map(warn.__contains__,agree)):
                                continue
                #execution block
                queryresult=db.queryexec(cur,query)
                if not queryresult[1]==1:
                    note["false"].append(query)
                else:
                    note["true"].append(query)
        con.commit()
        con.close()
        return None

    #noop
    def from_row(db):
        con=sqlite3.connect(db)
        cur=con.cursor()
        cur.executescript('''
        drop table if exist tableName;
        create table pkr(
            "id" text,
            "name0" text,
            "name1" text,
            "name2" text,
            "name3" text,
            "cat0" text,
            "cat1" text,
            "cat2" text,
            "cat3" text,
            "price0" INTEGER,
            "price1" INTEGER
            )
        ''')
        #get default csvfile name
        if len(csvfilename)==0:
            csvfilename='csvfile.csv'
        #get csvfile
        with open(csvfilename,newline='') as csvfile:
            r=csv.reader(csvfile,delimiter=',')
            #have per-line iterables
            for line in r:
                #set per-column scalars in the row
                print(line)
                id=line[0]
                name0=line[1]
                name1=line[2]
                name2=line[3]
                name3=line[4]
                cat0=line[5]
                cat1=line[6]
                cat2=line[7]
                cat3=line[8]
                price0=int(line[9])
                price1=int(line[10])
                #qmark style insertion https://dev.mysql.com/doc/refman/8.0/en/insert.html
                cur.execute('''
                insert into pkr(
                    id,
                    name0,
                    name1,
                    name2,
                    name3,
                    cat0,
                    cat1,
                    cat2,
                    cat3,
                    price0,
                    price1
                    )
                values (?,?,?,?,?,?,?,?,?,?,?)
                ''',(
                    id,
                    name0,
                    name1,
                    name2,
                    name3,
                    cat0,
                    cat1,
                    cat2,
                    cat3,
                    price0,
                    price1
                    ))
                con.commit()