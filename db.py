import sqlite3
from sqlite3.dbapi2 import Error

def conectar():
    dbname= 'imagenes.db'
    conn= sqlite3.connect(dbname)
    return conn

def getUser(user):
    conn= conectar()
    cursor= conn.execute("select * from tbl_Users WHERE user = '"+ user +"';")
    resultados= list(cursor.fetchall())
    conn.close()
    return resultados

def getPosts():
    conn= conectar()
    cursor= conn.execute("select * from imagenes ORDER BY codigo DESC;")
    resultados= list(cursor.fetchall())
    conn.close()
    return resultados
  
def getPostByUser(user):
    conn= conectar()
    cursor= conn.execute("select * from imagenes WHERE user = '"+ user +"' ORDER BY codigo DESC;")
    resultados= list(cursor.fetchall())
    conn.close()
    return resultados

def addPost(url, code, status, user):
    try :
        conn=conectar()
        conn.execute("insert into imagenes (url, codigoPost, mensaje, user) values(?,?,?,?);", (url, code, status, user))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False
    


