import sqlite3
import csv
import numpy as np
#https://www.sqlite.org/about.html
#https://docs.python.org/3/library/sqlite3.html

#pd.DataFrame.to_sql(
#    name=tableName
#    con=sqlite3.Connection,sqlalchemy.engine
#    index=True
#    index_label=[df.index.names]
#)

#connect to the databaseName, get a Connetion object
database=sqlite3.connect('databaseName')
#from the Connection object get a Cursor object
currentPosition=database.cursor()
#https://www.sqlite.org/datatype3.html
#create a table, designate columns
currentPosition.executescript('''
drop table if exist tableName;
create table "tableName"(
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
#get csvfile name
csvfilename=input('csvfile name: ')
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
        price0=np.uint64(line[9])
        price1=np.uint64(line[10])
        #qmark style insertion https://dev.mysql.com/doc/refman/8.0/en/insert.html
        currentPosition.execute('''
        INSERT INTO tableName(
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
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
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
        database.commit()
database.close()