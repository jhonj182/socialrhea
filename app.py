from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify
from flask_bcrypt import Bcrypt
from flask.helpers import url_for
import os
import db
import json
from werkzeug.utils import secure_filename
import utils
import validacion as valida
from datetime import date
from datetime import datetime

UPLOAD_FOLDER = 'static/uploads'
UPLOAD_IMG_FOLDER = 'static/uploads/imgusuarios'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_IMG_FOLDER'] = UPLOAD_IMG_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/upload/<user>', methods=['GET', 'POST'])
def upload_post(user):
  if request.method == 'POST':
    files = request.files.getlist("file[]")
    Titulo = request.form['TituloPost']
    status = request.form['status-input']
    visibilidad = request.form['Visibilidad']
    idUser = request.form['idUser']
    filenames = []
    estado = db.addPost(idUser, status, Titulo, visibilidad)
    for file in files:
      filename = secure_filename(file.filename)
      try:
          working_directory = 'static'
          file.save(working_directory + "/uploads/" + filename)
          filenames.append(filename)
      except FileNotFoundError :
          return 'Error, folder does not exist'
    arregloImagenes = ",".join(filenames)
    print(arregloImagenes)
    if estado:
          arreglo = arregloImagenes.split(',')
          for imagen in arreglo:
            db.addFoto(idUser, imagen)
          return redirect(f'/feed/{user}')
    else :
        return "<h1>Fallo proceso de Registro.</h1>" 

@app.route('/', methods=['GET', 'POST'])
def login():
  error = ""
  if request.method == 'POST':
    username = request.form['login-email']
    password = request.form['login-password']
    dbUsuario = db.getUser(username)
    pw_hash = dbUsuario['Contrasena']
    check = bcrypt.check_password_hash(pw_hash, password) # returns True
    if dbUsuario['Usuario'] == username and check :
      session["usuario"] = username
      return redirect('feed/'+username)
    else:
      error = "usuario o clave invalidos"
      flash(error, 'error')
      return render_template('login.html');
  else:
      flash("Por favor iniciar sesion", 'error')
      return render_template('login.html');
    
    # return jsonify({"encontrado" : encontrado})

@app.route('/logout')
def logout():
  session['usuario'] = None
  return redirect("/")

@app.route('/feed/<user>')
def main_page(user):
  dbUsuario = db.getUser(user)
  if(dbUsuario):
    idUser = dbUsuario['ID_Usuario']
    output = db.getPosts(4)
    
    print(output.get('ID_Post'))
    usuarios = db.getUsers(dbUsuario['ID_Usuario'])
    return render_template('feed.html', usuario=dbUsuario, usuarios = usuarios, output = output)
  else:
    return redirect('/')

@app.route('/profile/<user>', methods=['GET', 'POST'])
def profile(user):
  dbUsuario = db.getUser(session['usuario'])
  usuarios = db.getUsers(dbUsuario['ID_Usuario'])
  session['usuario'] = user
  auth = False
  db.getPosts(dbUsuario['ID_Usuario'])
  if user == session['usuario']:
    auth = True
    output = db.getPostByUser(dbUsuario['ID_Usuario'])
    print (output)
    jsonStr = json.dumps(output)
    return render_template('perfil.html', usuario=dbUsuario, output=output, auth=auth, usuarios = usuarios)
  else:
    output = db.getPostByUser(user)
    dbUsuario2 = db.getUser(user)
    relacion = db.getRelacion(dbUsuario['id_usuario'], dbUsuario2['id_usuario'])
    if dbUsuario2['Usuario'] == user:
      usr = True
    print (relacion)
    return render_template('perfil.html', usuario=dbUsuario, output=output, auth=auth, res=dbUsuario2, usuarios = usuarios, relacion=relacion)

@app.route('/agregaramigo/<user>', methods=['GET'])
def crearAmigo(user):
    nuevoAmigo = db.getUser(user)
    print(dbUsuario)
    print(nuevoAmigo)
    db.addAmigo(dbUsuario['id_usuario'], nuevoAmigo['id_usuario'])
    return redirect(f'/profile/{user}')

@app.route('/eliminaramigo/<user>', methods=['GET'])
def eliminarAmigo(user):
    nuevoAmigo = db.getUser(user)
    answer = db.deleteRelacion(dbUsuario['id_usuario'], nuevoAmigo['id_usuario'])
    if answer:
      flash('No se pudo eliminar', 'error')
      return redirect(f'/profile/{user}')
    else:
      flash('si se pudo eliminar', 'success')
      return redirect(f'/profile/{user}')

@app.route('/mensajes/<user>/<recept>', methods=['GET', 'POST'])
def busqueda_msg(user, recept):
  dbUsuario = db.getUser(user)
  usuarios = db.getUsers(dbUsuario['ID_Usuario'])
  rece = db.getUser(recept)
  mensajes = db.getMensaje(dbUsuario['ID_Usuario'], rece['ID_Usuario'])
  if request.method == "POST":
    mensaje = request.form['mensaje']
    db.addMensaje(dbUsuario['ID_Usuario'], rece['ID_Usuario'], mensaje )
    mensajes = db.getMensaje(dbUsuario['ID_Usuario'], rece['ID_Usuario'])
    return render_template('mensajes.html', usuario=dbUsuario, receptor=rece, mensajes=mensajes,  usuarios = usuarios)
  else:
    return render_template('mensajes.html', usuario=dbUsuario, receptor=rece, mensajes=mensajes,  usuarios = usuarios)
  # return render_template('')

@app.route('/busqueda/<user>', methods=["GET","POST"])
def busqueda(user):
  usr = []
  session['usuario'] = user
  dbUsuario = db.getUser(user)
  print(dbUsuario)
  if request.method == 'POST':
    resultado = request.form['busqueda']
    respuesta = db.getUsersByName(resultado)
    return render_template('busqueda.html', usuario=dbUsuario, respuestas=respuesta)
  else:
    return redirect('/feed')

@app.route('/amigos/')
def amigo():
  return redirect('/feed/<session["usuario"]>')

@app.route('/amigos/<user>')
def amigos(user):
  usr = []
  session['usuario'] = user
  if user == session['usuario']:
  
    if request.method == 'GET':
      resultado = db.getUsers(dbUsuario['ID_Usuario'])
      return render_template('amigos.html', usuario=dbUsuario, respuestas=resultado)
  else:
    return redirect('login', usuario=usr)

@app.route('/fotos/<user>', methods=['GET', 'POST'])
def fotos(user):
  session['usuario'] = user
  if user == session['usuario']:
    output = db.getPosts()
    return render_template('fotos.html', usuario=dbUsuario, respuestas=output)
  else:
    return redirect('/feed', session['usuario'])

@app.route('/deletePost/<idPost>')
def deletePost(idPost):
  usr = session['usuario']
  post = db.getPostById(idPost)
  cadena = post[1].split(',')
  if(db.deletePost(idPost)):
    for c in cadena:
      if(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], c))):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], c))
    return redirect('/fotos/'+ usr)
  else:
    flash('No se pudo eliminar', 'error')
    return redirect('/fotos/'+ usr)
  pass

@app.route('/admin/<user>', methods=['GET', 'POST'])
def admin(user):
  if user == 'admin':
    print(dbUsuario)
    print(session["usuario"])
    return render_template('dashboard.html', usuario=dbUsuario)
  else:
    return redirect('/')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
  error = ""
  usr = False
  if request.method == 'POST':
    username = request.form['login-email']
    password = request.form['login-password']
    select = request.form['select']
    dbUsuario = db.getUser(username)
    
    if username == dbUsuario['Usuario'] and password == 'admin':
      session["usuario"] = 'john_tama'
      dbUsuario= dbUsuario
      print(dbUsuario)
      return redirect('admin/'+username)
    else:
      error = "usuario o clave invalidos"
      flash(error, 'error')
      return render_template('admin-login.html');
  else:
    flash("Por favor iniciar sesion", 'error')
    return render_template('admin-login.html');


@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
  if session['usuario']:
    usuarios = db.getUsers(dbUsuario['ID_Usuario'])
    return render_template('dashboard-users.html', usuario=dbUsuario, usuarios=usuarios)

@app.route('/admin/superusers', methods=['GET', 'POST'])
def admin_superusers():

  if session['usuario']:
    usuarios = db.getSuperUsers()
    return render_template('dashboard-superuser.html', usuario=dbUsuario, usuarios=usuarios)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/deleteuser/<user>')
def deleteUser(user):
  if session['usuario']:
    if db.deleteUser(user):
      flash('Usuario eliminado con éxito', 'success')
      return redirect('/admin/users')
    else:
      flash("no se pudo eliminar", 'error')
      return redirect('/admin/users')


@app.route('/deleteadmin/<user>')
def deleteAdmin(user):
  if session['usuario']:
    if db.deleteAdmin(user):
      flash('Usuario Administrador eliminado con éxito', 'success')
      return redirect('/admin/superusers')
    else:
      flash("no se pudo eliminar", 'error')
      return redirect('/admin/superusers')
  pass
#DBERNAL - Registro de nuevo usuario en la red social
@app.route('/registro', methods=['GET', 'POST'])
def Nuevo_Usuario():
  if request.method == 'POST':
    nombres = request.form['Nombres']
    apellidos = request.form['Apellidos']
    usuario = request.form['Usuario']
    password = request.form['Password']
    rpassword = request.form['Rpassword']
    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
    genero = request.form['Genero']
    Estado_Civil = request.form['Estado_Civil']
    email = request.form['Email']
    pais = request.form['Pais']
    telefono = request.form['Telefono']
    privacidad = request.form['Privacidad']
    nacimiento = request.form['FechaN']
    error = None
    if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename))
    if password != rpassword:
      error = "Las contraseñas son diferentes"
      flash(error)
      return render_template('registro2.html')

    if not utils.isUsernameValid(usuario):
      error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
      flash(error)
      return render_template('registro2.html')

    if not utils.isPasswordValid(password):
      error = 'La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres'
      flash(error)
      return render_template('registro2.html')

    if not utils.isEmailValid(email):
      error = 'Correo invalido'
      flash(error)
      return render_template('registro2.html')
    db.addUser(usuario, hash_password, nombres, apellidos, genero, email, pais, filename, telefono , nacimiento, Estado_Civil, privacidad)
    session["usuario"] = usuario
    return redirect('feed/'+session["usuario"])

  else:    
    return render_template('registro2.html')

@app.route('/admin/createadmin', methods=['GET', 'POST'])
def Nuevo_Admin():
  if request.method == 'POST':
    nombres = request.form['Nombres']
    apellidos = request.form['Apellidos']
    usuario = request.form['Usuario']
    password = request.form['Password']
    hash_password = bcrypt.generate_password_hash(password)
    rpassword = request.form['Rpassword']
    email = request.form['Email']
    pais = request.form['Pais']
    error = None
    if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename))
    if password != rpassword:
      error = "Las contraseñas son diferentes"
      flash(error)
      return render_template('createadmin.html', usuario=dbUsuario)

    if not utils.isUsernameValid(usuario):
      error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
      flash(error)
      return render_template('createadmin.html', usuario=dbUsuario)

    if not utils.isPasswordValid(password):
      error = 'La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres'
      flash(error)
      return render_template('createadmin.html', usuario=dbUsuario)

    if not utils.isEmailValid(email):
      error = 'Correo invalido'
      flash(error)
      return render_template('createadmin.html', usuario=dbUsuario)
    db.addAdmin(usuario, nombres, hash_password, filename, filename, pais)
    session["usuario"] = usuario
    return redirect('/admin/superusers')
  else:    
    return render_template('createadmin.html', usuario=dbUsuario)

@app.route('/updateperfil', methods=['GET', 'POST'])
def updateperfil():
  usuario = session['usuario']
  if request.method == 'POST':
    nombres = request.form['Nombres']
    apellidos = request.form['Apellidos']
    password = request.form['Password']
    rpassword = request.form['Rpassword']
    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
    Estado_Civil = request.form['Estado_Civil']
    email = request.form['Email']
    pais = request.form['Pais']
    telefono = request.form['Telefono']
    nacimiento = request.form['FechaN']
    error = None
    if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename))
    if password != rpassword:
      error = "Las contraseñas son diferentes"
      flash(error)
      return redirect('editarperfil')

    if not utils.isPasswordValid(password):
      error = 'La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres'
      flash(error)
      return redirect('editarperfil')

    if not utils.isEmailValid(email):
      error = 'Correo invalido'
      flash(error)
      return redirect('editarperfil')
    dbUsuario = db.getUser(session['usuario'])
    print(dbUsuario['ID_Usuario'])
    print(usuario)
    print(usuario)
    print(usuario)
    print(usuario)
    print(dbUsuario['ID_Usuario'])
    print(dbUsuario['ID_Usuario'])
    print(dbUsuario['ID_Usuario'])
    print(dbUsuario['ID_Usuario'])
    db.updateUser(dbUsuario['ID_Usuario'], nombres, apellidos, hash_password, Estado_Civil, email, pais, filename, telefono , nacimiento)
    session["usuario"] = usuario
    return redirect('editarperfil')
  else:    
    return redirect('editarperfil')

@app.route('/editarperfil', methods=['GET', 'POST'])
def editarperfil():
  dbUsuario = db.getUser(session['usuario'])
  return render_template('editarPerfil.html', usuario=dbUsuario)

#DBERNAL - Recuperación de credenciales
@app.route('/olvidar')
def RecuperaU():
    return render_template('olvidar.html', methods=('POST'))
  
# @app.before_request
# def antes_de_cada_peticion():
#     ruta = request.path
#     # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
#     if not 'usuario' in session and ruta != "/" and ruta != "/admin-login" and ruta != "/logout" and not ruta.startswith("/static"):
#         flash("Inicia sesión para continuar")
#         return redirect("/")
#     # Si ya ha iniciado, no hacemos nada, es decir lo dejamos pasar

# Main
if __name__=='__main__':
    app.run(debug=True, port=5500)
