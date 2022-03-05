import csv
import sqlite3
import pandas as pd
class db:
    #db.csv_to
    def csv_to(
        db:str="c:/code/db.db",
        chk:bool=False,
        use:bool=False
        ):
        #get a connect object, cursor object
        con=sqlite3.connect(f"{db}")
        cur=con.cursor()
        #have csv
        while True:
            csvfilename=input("csvfile path: ")
            if not csvfilename:
                break
            df=pd.read_csv(csvfilename)
            print(f"loaded: {csvfilename} {df.shape}")
            tablename=input("tablename: ")
            df.to_sql(
                tablename,
                con=con,
                if_exists="replace",
                index_label=f"idx_{tablename}"
            )
            if chk:
                list(map(print,{q[1][1] for q in enumerate(
                cur.execute(f'select * from {tablename}'))}))
            print(f"success: {csvfilename} -> {db} -> {tablename}")
        if use:
            return cur
        else:
            #pd.to_sql automatically commits
            con.close()
            return None
    #db.query
    def query()->None:
        dbname=input("db: ")
        if not dbname:
            dbname="c:/code/db.db"
        with sqlite3.connect(f"{dbname}") as con:
            cur=con.cursor()
            exe=cur.execute
            print(f"connected: {dbname}")
            while dbname:
                userquery=input(f"{dbname}->")
                if not userquery:
                    cur.close()
                    break
                if userquery.startswith("select"):
                    cache=exe(f"{userquery}").fetchall()
                    rowslen=len(cache)
                    if rowslen>99:
                        print(f"{cache[:99]}\nremaining: {rowslen-99}")
                    else:
                        print(f"{cache}\nrows: {rowslen}")
                else:
                    exe(f"{userquery}")
        con.close()
        return None

def ppp():
    return None

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
