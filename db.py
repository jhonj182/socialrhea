import sqlite3
from sqlite3.dbapi2 import Error

def conectar():
    dbname= 'imagenes.db'
    conn= sqlite3.connect(dbname)
    return conn

def getImagenes():
    conn= conectar()
    cursor= conn.execute("select * from imagenes ORDER BY codigo DESC;")
    resultados= list(cursor.fetchall())
    conn.close()
    return resultados

def addProducto(url, code, status):
    try :
        conn=conectar()
        conn.execute("insert into imagenes (url, codigoPost, mensaje) values(?,?,?);", (url, code, status))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False
    


