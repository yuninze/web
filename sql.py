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
    def to_db(db:str="c:/code/db.db",
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
                list(map(print,{q[1][1] for q in enumerate(
                cur.execute(f'select * from {tablename}'))}))
            print(f"success: {filename} -> {db} -> {tablename}")
        if use:
            return cur
        else:
            con.close() #pd.to_sql automatically commits
            return None
    #db.queryexec
    def queryexec(cur,
            query:str)->tuple:
        try:
            return cur.execute(query),1
        except (sqlite3.ProgrammingError,
                sqlite3.OperationalError,
                sqlite3.NotSupportedError) as e:
            return print(f"->{e} '{query}'"),2
    #db.query
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

def ppp():
    return None

# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id SERIAL PRIMARY KEY, 
    start_time bigint NOT NULL, 
    user_id int NOT NULL, 
    level varchar, 
    song_id varchar, 
    artist_id varchar, 
    session_id int, 
    location varchar, 
    user_agent varchar
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id int PRIMARY KEY, 
    first_name varchar, 
    last_name varchar, 
    gender varchar, 
    level varchar);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id varchar PRIMARY KEY, 
    title varchar, 
    artist_id varchar, 
    year int, 
    duration float
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id varchar PRIMARY KEY, 
    name varchar, 
    location varchar, 
    latitude float, 
    longitude float
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time bigint PRIMARY KEY, 
    hour int, 
    day int, 
    week int, 
    month int, 
    year int, 
    weekday int
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (
    start_time, 
    user_id, 
    level, 
    song_id, 
    artist_id, 
    session_id, 
    location, 
    user_agent
) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users (
    user_id, 
    first_name, 
    last_name, 
    gender, 
    level
) 
VALUES (%s, %s, %s, %s, %s) 
ON CONFLICT (user_id) DO SET level = EXCLUDED.level;
""")

song_table_insert = """
INSERT INTO songs (
    song_id, 
    title, 
    artist_id, 
    year, 
    duration
) 
VALUES (%s, %s, %s, %s, %s) 
ON CONFLICT (song_id) DO NOTHING
"""

artist_table_insert = ("""
INSERT INTO artists (
    artist_id, 
    name, 
    location, 
    latitude, 
    longitude
) 
VALUES (%s, %s, %s, %s, %s) 
ON CONFLICT (artist_id) DO NOTHING
""")


time_table_insert = ("""
INSERT INTO time (
    start_time, 
    hour, 
    day, 
    week, 
    month, 
    year, 
    weekday
) 
VALUES (%s, %s, %s, %s, %s, %s, %s) 
ON CONFLICT (start_time) DO NOTHING
""")

# FIND SONGS

song_select = ("""
SELECT song_id, artists.artist_id FROM songs 
INNER JOIN artists ON artists.artist_id = songs.artist_id
WHERE title = (%s) AND name = (%s) AND duration = (%s)
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

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
