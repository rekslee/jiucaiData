import pandas as pd
import sqlite3

def checkTalbe(conn,table):
    cur = conn.cursor()
    check_cmd = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name = '{}'".format(table)
    cur.execute(check_cmd)
    result = cur.fetchone()
    cur.close()
    return result[0]
    
def dataToDB(db,data,table):
    if isinstance(data,list):
        conn = sqlite3.connect(db)
        while data:
            df = data[0]
            df.to_sql(df['code'].values[0], conn,if_exists="replace" ,index=False)
            data.pop(0)
        conn.close()
    else:
        conn = sqlite3.connect(db)
        data.to_sql(table, conn,if_exists="replace" ,index=False)
        conn.commit()
        conn.close()
        print(table,"saved to DB")

def readDB(db,table,num=0):
    if num<0:
        sql_cmd = "select * from 'tablename' ORDER BY 'date' DESC LIMIT {}".format(abs(num))
    elif num>0:
        sql_cmd = "select * from 'tablename' ORDER BY 'date' LIMIT {}".format(abs(num))
    else:
        sql_cmd = "select * from 'tablename'"
    if isinstance(table,list):
        data_list=[]
        conn = sqlite3.connect(db)
        while table:
            symbol = table[0]
            # print('read',symbol)
            if checkTalbe(conn,symbol):
                table_cmd=sql_cmd.replace('tablename',symbol)
                data_list.append(pd.read_sql(sql=table_cmd, con=conn))
            else:
                data_list.append(None)
            table.pop(0)
        conn.close()
        return data_list
    else:
        conn = sqlite3.connect(db)
        if checkTalbe(conn,table):
            table_cmd=sql_cmd.replace('tablename',table)
            data = pd.read_sql(sql=table_cmd, con=conn)
            conn.close()
            return data
        else:
            conn.close()
            return None

    