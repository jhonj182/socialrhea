import sqlite3
from sqlite3.dbapi2 import Error

def conectar():
    dbname= 'imagenes.db'
    conn= sqlite3.connect(dbname)
    return conn

def getUser(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("select * from tbl_Users WHERE User = '"+ user +"';")
      resultados = dict(cursor.fetchone())
      if not resultados:
        print ('Login failed')
      else:
        return resultados
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )
    finally:
        if conn:
            cursor.close()
            conn.close()

def getUsersByName(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("select * from tbl_Users WHERE name like '%"+ user +"%';")
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      conn.close()
      return results
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )

def getUsers():
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("select * from tbl_Users;")
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      conn.close()
      return results
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )

def getSuperUsers():
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("select * from tbl_Users;")
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      conn.close()
      return results
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )

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
    


