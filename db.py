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
        return False
      else:
        return resultados
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )
    finally:
        if conn:
            cursor.close()
            conn.close()

def getUserAdmin(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("select * from tbl_admin WHERE User = '"+ user +"';")
      resultados = dict(cursor.fetchone())
      print(resultados)
      print(resultados)
      print(resultados)
      print(resultados)
      print(resultados)
      print(resultados)
      if not resultados:
        print ('Login failed')
        return False
      else:
        return resultados
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )
    finally:
        if conn:
            cursor.close()
            conn.close()

def getUserSuperAdmin(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("select * from tbl_super_admin WHERE User = '"+ user +"';")
      resultados = dict(cursor.fetchone())
      print('asdasdljkahsdlkjashdflrqzhonksmrqzkhoms;halsdk qozshkrqm;ozshkrqm;oshzrkq;oshzrkqo; lkjasdhflkasjdo;')
      print(cursor)
      print(cursor)
      print(cursor)
      print(cursor)
      print(cursor)
      print(cursor)
      print(cursor)
      print(cursor)
      if not resultados:
        print ('Login failed')
        return False
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
      cursor= conn.execute("select * from tbl_admin;")
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

def getPostById(idPost):
    conn= conectar()
    sql = 'SELECT * from imagenes WHERE codigo = ?;'
    cursor= conn.execute(sql, (idPost,))
    resultados= list(cursor.fetchone())
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
    
def addUser(user, name, password, profPic, highPic, country):
    try :
        conn=conectar()
        conn.execute("insert into tbl_Users (user, name, passwrd, profPic, highPic, country) values(?,?,?,?,?,?);", (user, name, password, profPic, highPic, country))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False
      
def addAdmin(user, name, password, profPic, highPic, country):
    try :
        conn=conectar()
        conn.execute("insert into tbl_admin (user, name, passwrd, profPic, highPic, country) values(?,?,?,?,?,?);", (user, name, password, profPic, highPic, country))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False
      
def updateUser(user, nombres, password, filename, pais):
    try :
        print('entro')
        conn=conectar()
        conn.execute("UPDATE tbl_Users SET name=?, passwrd = ?, profPic = ?, country = ? WHERE user = ?;", (nombres, password, filename, pais, user))
        conn.commit()
        conn.close()
        print('actualizado')
        print('actualizado')
        print('actualizado')
        print('actualizado')
        return True
    except Error as error:
        print(error)
        print(error)
        print(error)
        print(error)
        return False
    
def deleteUser(user):
    try :
        conn=conectar()
        sql = 'DELETE FROM tbl_Users WHERE User = ?'
        conn.execute(sql, (user,))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False

def deleteAdmin(user):
    try :
        conn=conectar()
        sql = 'DELETE FROM tbl_admin WHERE User = ?'
        conn.execute(sql, (user,))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False
    

def deletePost(idPost):
    try :
        conn=conectar()
        sql = 'DELETE FROM imagenes WHERE codigo = ?'
        conn.execute(sql, (idPost,))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False
    


