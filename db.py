import sqlite3
from sqlite3.dbapi2 import Error

def conectar():
    dbname= '/home/jtamayoj182/mysite/socialrhea/socialrhea/SocialRhea.db'
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
    except:
      print("error in getUser() "  )

def getUserAdmin(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("SELECT * FROM tbl_admin WHERE User = '"+ user +"';")
      resultados = dict(cursor.fetchone())
      if not resultados:
        return False
      else:
        return resultados
    except:
      print("error in getUserAdmin() "  )
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
    except:
      print("error in getUserSuperAdmin() "  )
    finally:
        if conn:
            cursor.close()
            conn.close()

def getUsersByName(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("SELECT * FROM Usuario WHERE nombres like '%"+ user +"%';")
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      conn.close()
      return results
    except:
      print("error in getUsersbyname() "  )

def getAmigos(idUsuario):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sq = 'SELECT Amistad.ID_Recibe, Amistad.ID_Envia FROM Usuario INNER JOIN Amistad ON Amistad.ID_Envia=Usuario.ID_Usuario or Amistad.ID_Recibe=Usuario.ID_Usuario WHERE Usuario.ID_Usuario = ? and Amistad.Estado = 1'
      sql = 'SELECT * FROM Usuario WHERE rol=? AND Not ID_Usuario = ?'
      cursor= conn.execute(sq,(idUsuario,))
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      resultados = getUsers(results, conn, idUsuario)
      return resultados
    except:
      print("error in getUserees() "  )

def getUsers(listaAmigos, conn, idUsuario):
    salida = []
    try:
      conn.row_factory = sqlite3.Row
      for item in listaAmigos:
        for key, value in item.items():
          sql = 'SELECT * FROM Usuario WHERE ID_Usuario = ? AND NOT ID_Usuario = ?'
          cursor= conn.execute(sql,(value, idUsuario))
          resultado = (cursor.fetchone())
          if resultado:
            results = dict(resultado)
            salida.append(results)
      # results = [ dict(row) for row in resultado ]
      conn.close()
      return salida
    except:
      print("error in getUsers() "  )

def getPostsFeed(idUsuario, listaAmigos):
    conn= conectar()
    salida = []
    # print(listaAmigos)
    conn.row_factory = sqlite3.Row
    sql = 'SELECT * FROM Post WHERE ID_Usuario = ? ORDER BY ID_Post asc'
    cursor= conn.execute(sql,(idUsuario,))
    resultado = (cursor.fetchall())
    if resultado:
      results = [ dict(row) for row in resultado ]
      salida.append(results)
    try:
      for item in listaAmigos:
        for key, value in item.items():
          if key == 'ID_Usuario':
            sql = 'SELECT * FROM Post WHERE ID_Usuario = ? ORDER BY ID_Post asc'
            cursor= conn.execute(sql,(value,))
            resultado = (cursor.fetchall())
            if resultado:
              results = [ dict(row) for row in resultado ]
              salida.append(results)
              # results = [ dict(row) for row in resultado ]
      fotos = getFotos(conn, salida)
      return fotos
    except:
      print("error in getPostsFeed() "  )

def getPostsMe(idUsuario):
    conn= conectar()
    salida = []
    # print(listaAmigos)
    conn.row_factory = sqlite3.Row
    try:
      sql = 'SELECT * FROM Post WHERE ID_Usuario = ?'
      cursor= conn.execute(sql,(idUsuario,))
      resultado = (cursor.fetchall())
      if resultado:
        results = [ dict(row) for row in resultado ]
        salida.append(results)
      fotos = getFotos(conn, salida)
      return fotos
    except:
      print("error in getPostsFeed() "  )

def getAllUsers():
    conn= conectar()
    conn.row_factory = sqlite3.Row
    try:
      sql = 'SELECT * FROM Usuario WHERE Rol = ?'
      cursor= conn.execute(sql,(2,))
      resultado = (cursor.fetchall())
      if resultado:
        results = [ dict(row) for row in resultado ]
      return results
    except:
      print("error in getPostsFeed() "  )

def getAllAdmins():
    conn= conectar()
    conn.row_factory = sqlite3.Row
    try:
      sql = 'SELECT * FROM Usuario WHERE Rol = ?'
      cursor= conn.execute(sql,(1,))
      resultado = (cursor.fetchall())
      if resultado:
        results = [ dict(row) for row in resultado ]
      return results
    except:
      print("error in getPostsFeed() "  )

def getAllSuperAdmins():
    conn= conectar()
    conn.row_factory = sqlite3.Row
    try:
      sql = 'SELECT * FROM Usuario WHERE Rol = ?'
      cursor= conn.execute(sql,(0,))
      resultado = (cursor.fetchall())
      if resultado:
        results = [ dict(row) for row in resultado ]
      return results
    except:
      print("error in getPostsFeed() "  )

def getFotos(conn, salida):
    salidaFotos = []
    salidaPosts = {}
    salidaPosts2 = []
    for item1 in salida:
      for item in item1:
        salidaPosts['post']=(item)
        for key, value in item.items():
          if key == 'ID_Usuario':
            sql = 'SELECT ID_Usuario, Nombres, Foto FROM Usuario WHERE ID_Usuario = ?'
            cursor= conn.execute(sql,(value,))
            resultado = (cursor.fetchone())
            results = dict(resultado)
            if resultado:
              salidaPosts['Usuario']=(results)
              # results = [ dict(row) for row in resultado ]
          if key == 'ID_Post':
            sql = 'SELECT ID_Foto, ID_Post, Ruta FROM Foto WHERE ID_Post = ?'
            cursor= conn.execute(sql,(value,))
            resultado = (cursor.fetchall())
            results = [ dict(row) for row in resultado ]
            if resultado:
              salidaPosts['fotos']=(results)
              salidaFotos.append(results)
              # results = [ dict(row) for row in resultado ]
              salidaPosts2.append(salidaPosts)
              salidaPosts={}
    conn.close()
    return(salidaPosts2)
# def getFotos(conn, salida):
#     salidaFotos = []
#     salidaPosts = {}
#     salidaPosts2 = []
#     for item1 in salida:
#       for item in item1:
#         salidaPosts['post']=(item)
#         for key, value in item.items():
#           if key == 'ID_Post':
#             sql = 'SELECT * FROM Foto WHERE ID_Post = ?'
#             cursor= conn.execute(sql,(value,))
#             resultado = (cursor.fetchall())
#             results = [ dict(row) for row in resultado ]
#             if resultado:
#               salidaPosts['fotos']=(results)
#               print("/////// post {value} ////")
#               print(salidaPosts)
#               print("/////// endpost {value} ////")
#               salidaFotos.append(results)
#               # results = [ dict(row) for row in resultado ]
#               salidaPosts2.append(salidaPosts)
#     conn.close()
#     print('salidaPosts2')
#     print(salidaFotos)
#     return(salidaFotos)


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
    except:
      print("error in getMensaje() "  )
      return(False)


def getRelacion(emisor, receptor):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sql = 'SELECT * FROM Amistad where (ID_Envia = ? AND ID_Recibe = ?) or (ID_Envia = ? AND ID_Recibe = ?) ORDER BY ID_Solicitud DESC'
      cursor= conn.execute(sql, (emisor, receptor, receptor, emisor))
      resultado = (cursor.fetchone())
      results = dict(resultado)
      conn.close()
      if (results):
        return results
      else:
        return False
    except:
      print("error in getRelacion() "  )

def updateRelacion(emisor, receptor, estado):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sql = 'UPDATE Amistad SET Estado = ? where (ID_Envia = ? AND ID_Recibe = ?)'
      conn.execute(sql, (estado ,emisor, receptor,))
      conn.commit()
      conn.close()
      return True
    except:
      print("error in updateRelacion() "  )
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
    except:
      print("error in getSuperUser() "  )

def getPosts(idUsuario):
    try:
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
    except:
      return False

def getPostByUser(idUser):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sql = 'SELECT * FROM Post WHERE ID_Usuario = ? ORDER BY ID_Post DESC;'
      cursor= conn.execute(sql, (idUser,))
      resultado = (cursor.fetchall())
      resultados= [ dict(row) for row in resultado ]
      conn.close()
      return resultados
    except:
      return False



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
    except:
        return False

def getLastPostId(idUser):
  conn= conectar()

  try:
    sql = 'SELECT ID_Post FROM Post WHERE ID_Post = (SELECT MAX(ID_Post) FROM Post) AND ID_Usuario = ?; '
    cursor= conn.execute(sql, (idUser,))
    resultados= (cursor.fetchone())
    conn.close()
    return resultados[0]
  except:
      print("error en get post by iduser: {error}")
      return False

def addFoto(idUser, imagen):
    ID_Post = getLastPostId(idUser)
    try:
      conn=conectar()
      conn.execute("INSERT INTO Foto (ID_Post, Ruta) values(?,?);", (ID_Post, imagen))
      conn.commit()
      conn.close()
      return True
    except:
      print("imagen no agregada{imagen}: {error}")
      return False

def addMensaje(remitente, receptor, contenido):
    try :
        conn=conectar()
        conn.execute("INSERT into Mensajes_Privados (ID_Remitente, ID_Destinatario, Mensaje) values(?,?,?);", (remitente, receptor, contenido))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def addUser(usuario, password, nombres, apellidos, genero, email, pais, Foto, telefono , nacimiento, Estado_Civil, privacidad, rol):
    estado = 1
    try :
        conn=conectar()
        conn.execute("INSERT INTO Usuario (Usuario, Contrasena, Rol, Estado, Nombres, Apellidos, Genero, Email, Ubicacion, Foto, Telefono, Fecha_Nacimiento, Estado_Civil, Privacidad ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (usuario, password, rol, estado, nombres, apellidos, genero, email, pais, Foto, telefono , nacimiento, Estado_Civil, privacidad))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def updateUser(usuario, nombres, apellidos, password, Estado_Civil, email, pais, filename, telefono , nacimiento):
    try :
        conn=conectar()
        sql = 'UPDATE Usuario  SET Contrasena = ?, Nombres = ?, Apellidos = ?, Email = ?, Ubicacion = ?, Foto = ?, Telefono = ?, Estado_Civil = ?, Fecha_Nacimiento = ? WHERE ID_Usuario = ?'
        conn.execute(sql, (password, nombres, apellidos, email, pais, filename, telefono, Estado_Civil, nacimiento, usuario,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def updateUserAdmin(usuario, nombres, apellidos, Estado_Civil, email, pais, filename, telefono , nacimiento):
    try :
        conn=conectar()
        sql = 'UPDATE Usuario  SET  Nombres = ?, Apellidos = ?, Email = ?, Ubicacion = ?, Foto = ?, Telefono = ?, Estado_Civil = ?, Fecha_Nacimiento = ? WHERE ID_Usuario = ?'
        conn.execute(sql, (nombres, apellidos, email, pais, filename, telefono, Estado_Civil, nacimiento, usuario,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def addAdmin(user, name, password, profPic, highPic, country):
    try :
        conn=conectar()
        conn.execute("insert into tbl_admin (user, name, passwrd, profPic, highPic, country) values(?,?,?,?,?,?);", (user, name, password, profPic, highPic, country))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def addAmigo(envia, recibe):
    try :
        conn=conectar()
        conn.execute("INSERT into Amistad (ID_Envia, ID_Recibe) values(?,?);", (envia, recibe))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def deleteUser(user):
    try :
        conn=conectar()
        sql = 'DELETE FROM Usuario WHERE Usuario = ?'
        conn.execute(sql, (user,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def deleteAdmin(user):
    try :
        conn=conectar()
        sql = 'DELETE FROM Usuario WHERE Usuario = ?'
        conn.execute(sql, (user,))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def deletePost(idPost):
    try :
        conn=conectar()
        sql = 'DELETE FROM Post WHERE ID_Post = ?'
        conn.execute(sql, (idPost,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def deleteFoto(idFoto):
    try :
        conn=conectar()
        sql = 'DELETE FROM Foto WHERE ID_Foto = ?'
        conn.execute(sql, (idFoto,))
        conn.commit()
        conn.close()
        return True
    except:
        return False
