import sqlite3
from sqlite3.dbapi2 import Error

def conectar():
    dbname= 'socialrhea2.db'
    conn= sqlite3.connect(dbname)
    return conn

def getUser(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sql = 'SELECT * FROM Usuario WHERE Usuario = ?'
      cursor = conn.execute(sql, (user,))
      resultados = (cursor.fetchone())
      cursor.close()
      conn.close()
      if not resultados:
        return False
      else:
        return resultados
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )

def getFotos(Posts):
    dResultados = {}
    dList = []
    for post in Posts:
      # print(post)
      try:
        conn= conectar()
        token = post['token']
        print(token)
        conn.row_factory = sqlite3.Row
        sql = 'SELECT * FROM Foto WHERE token = ?'
        cursor = conn.execute(sql, (token,))
        resultados = (cursor.fetchall())
        results = [ dict(row) for row in resultados ]
        print(results)
        dResultados = results
        dList.append(dResultados)
        dResultados = {}
        conn.close()
      except Error as e:
        print(f"error in getFotos() : {str(e)}"  )
      print("Las fotos son:")
      print(dList)
      return(dList)

def getUserAdmin(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("SELECT * FROM tbl_admin WHERE User = '"+ user +"';")
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

def getUserSuperAdmin(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("SELECT * FROM tbl_super_admin WHERE User = '"+ user +"';")
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

def getUsersByName(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("SELECT * FROM tbl_Users WHERE nombre like '%"+ user +"%';")
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      conn.close()
      return results
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )

def getUsers(idUsuario):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sql = 'SELECT * FROM Usuario WHERE rol=? AND Not ID_Usuario = ?'
      cursor= conn.execute(sql,(2, idUsuario))
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      conn.close()
      return results
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )

def getMensaje(emisor, receptor):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sql = 'SELECT * FROM Mensajes_Privados where (ID_Remitente = ? OR ID_Remitente = ?) AND (ID_Destinatario = ? OR ID_Destinatario = ?);'
      cursor= conn.execute(sql, (emisor, receptor, receptor, emisor))
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      conn.close()
      return results
    except Error as e:
      print(f"error in getMensaje() : {str(e)}"  )
      return("false")


def getRelacion(emisor, receptor):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sql = 'SELECT * FROM Amistad where (id_envia = ? AND id_recibe = ?) AND (id_recibe = ? AND id_envia = ?);'
      cursor= conn.execute(sql, (emisor, receptor, receptor, emisor))
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      conn.close()
      if (results):
        return True
      else:
        return False
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )

def deleteRelacion(emisor, receptor):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sql = 'DELETE FROM Amistad where (id_envia = ? AND id_recibe = ?)'
      conn.execute(sql, (emisor, receptor,))
      conn.commit()
      conn.close()
      return True
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )
      return False

def getSuperUsers():
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("SELECT * FROM tbl_admin;")
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      conn.close()
      return results
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )

def getPosts(idUsuario):
    try:
      print("Esta Buscando el usuario: "+str(idUsuario))
      conn= conectar()
      conn.row_factory = sqlite3.Row
      sql = 'SELECT * FROM Foto INNER JOIN Post on Foto.ID_Post = Post.ID_Post and post.ID_Usuario = ?'
      cursor = conn.execute(sql, (idUsuario,))
      resultados= [ dict(row) for row in cursor ]
      for elem in resultados: #accedemos a cada elemento de la lista (en este caso cada elemento es un dictionario)
        for k,v in elem.items():        #acedemos a cada llave(k), valor(v) de cada diccionario
            if k == 'Ruta':
              print("claves del dict")
              print(k, v)
      print(resultados)
      conn.close()
      return resultados
    except Error as e:
      print(f"error in getPost() : {str(e)}"  )

def getPostByUser(idUser):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sql = 'SELECT * FROM Post WHERE ID_Usuario = ? ORDER BY ID_Post DESC;'
      cursor= conn.execute(sql, (idUser,))
      resultado = (cursor.fetchall())
      print (resultado)
      resultados= [ dict(row) for row in resultado ]
      conn.close()
      return resultados
    except Error as e:
      print(f"error in getMensaje() : {str(e)}"  )
      return("false")

  

def getPostById(idPost):
    conn= conectar()
    sql = 'SELECT * FROM imagenes WHERE codigo = ?;'
    cursor= conn.execute(sql, (idPost,))
    resultados= list(cursor.fetchone())
    conn.close()
    return resultados

def addPost(idUser, status, Titulo,  visibilidad):
    try :
        conn=conectar()
        conn.execute("INSERT INTO Post (ID_Usuario , Titulo, Visibilidad, Descripcion) values(?,?,?,?);", (idUser, Titulo, visibilidad, status))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False

def getLastPostId(idUser):
  conn= conectar()
  
  try:
    sql = 'SELECT ID_Post FROM Post WHERE ID_Post = (SELECT MAX(ID_Post) FROM Post) AND ID_Usuario = ?; '
    cursor= conn.execute(sql, (idUser,))
    resultados= (cursor.fetchone())
    conn.close()
    return resultados[0]
  except Error as error:
      print(f"error en get post by iduser: {error}")
      return False

def addFoto(idUser, imagen):
    ID_Post = getLastPostId(idUser)
    print(f"el id del post es {ID_Post}  {idUser}")
    try:
      conn=conectar()
      conn.execute("INSERT INTO Foto (ID_Post, Ruta) values(?,?);", (ID_Post, imagen))
      conn.commit()
      conn.close()
      print(f"imagen agregada{imagen}")
      return True
    except Error as error:
      print(f"imagen no agregada{imagen}: {error}")
      return False

def addMensaje(remitente, receptor, contenido):
    try :
        conn=conectar()
        conn.execute("INSERT into Mensajes_Privados (ID_Remitente, ID_Destinatario, Mensaje) values(?,?,?);", (remitente, receptor, contenido))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False
    
def addUser(usuario, password, nombres, apellidos, genero, email, pais, Foto, telefono , nacimiento, Estado_Civil, privacidad):
    rol = 2
    estado = 1
    try :
        conn=conectar()
        conn.execute("INSERT INTO Usuario (Usuario, Contrasena, Rol, Estado, Nombres, Apellidos, Genero, Email, Ubicacion, Foto, Telefono, Fecha_Nacimiento, Estado_Civil, Privacidad ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (usuario, password, rol, estado, nombres, apellidos, genero, email, pais, Foto, telefono , nacimiento, Estado_Civil, privacidad))
        conn.commit()
        conn.close()
        print('Registro Exitoso')
        return True
    except Error as error:
        print("error en Add User:", error)
        return False
      
def updateUser(usuario, nombres, apellidos, password, Estado_Civil, email, pais, filename, telefono , nacimiento):
    try :
        conn=conectar()
        sql = 'UPDATE Usuario  SET Contrasena = ?, Nombres = ?, Apellidos = ?, Email = ?, Ubicacion = ?, Foto = ?, Telefono = ?, Fecha_Nacimiento = ? WHERE ID_Usuario = ?'
        conn.execute(sql, (password, nombres, apellidos, email, pais, filename, telefono, Estado_Civil, nacimiento, usuario,))
        conn.commit()
        conn.close()
        print('Registro Exitoso')
        return True
    except Error as error:
        print("error en Add User:", error)
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
      
      
def addAmigo(envia, recibe):
    try :
        conn=conectar()
        conn.execute("INSERT into amistad (id_envia, id_recibe) values(?,?);", (envia, recibe))
        conn.commit()
        conn.close()
        return True
    except Error as error:
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
