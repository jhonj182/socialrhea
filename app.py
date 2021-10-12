from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify
from flask.helpers import url_for
from obtenerusuarios import usuarios
import os
import db
import json
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.secret_key = os.urandom(24)

@app.route('/upload/<user>', methods=['GET', 'POST'])
def upload_file(user):
  if request.method == 'POST':
    files = request.files.getlist("file[]")
    status = request.form['status-input']
    filenames = []
    for file in files:
      filename = secure_filename(file.filename)
      try:
          working_directory = 'static'
          file.save(working_directory + "/uploads/" + filename)
          filenames.append(filename)
      except FileNotFoundError :
          return 'Error, folder does not exist'
    a = ",".join(filenames)
    estado= db.addPost(a , "post", status, user)
    if estado:
          return redirect(f'/feed/{user}')
    else :
        return "<h1>Fallo proceso de insercion de Producto.</h1>" 

@app.route('/', methods=('GET', 'POST'))
def login():
  error = ""
  usr = False
  if request.method == 'POST':
    username = request.form['login-email']
    password = request.form['login-password']
    dbUser = db.getUser(username)
    if dbUser['User'] == username and dbUser['passwrd'] == password:
      usr = True
    if usr:
      session["usuario"] = username
      return redirect('feed/'+session["usuario"])
    else:
      error = "usuario o clave invalidos"
      flash(error, 'error')
      return render_template('login.html');
  else:
    flash("Por favor iniciar sesion", 'error')
    return render_template('login.html');
    
    # return jsonify({"encontrado" : encontrado})

@app.route('/feed/<user>', methods=('GET', 'POST'))
def main_page(user):
  usr = []
  dbUser = db.getUser(user)
  if dbUser['User'] == user:
    usr = True
    if usr:
      output = db.getPosts()
      return render_template('feed.html', usuario=dbUser, output=output)
  else:
    return redirect('/')
  
@app.route('/registro/<usuario>', methods=('GET', 'POST'))
def register(usuario):
  return render_template('login.html', usuario=usuario)

@app.route('/profile/<user>', methods=('GET', 'POST'))
def busqueda2(user):
  usr = []
  auth = False
  dbUser = db.getUser(session['usuario'])
  print(dbUser)
  if user == session['usuario']:
    auth = True
    output = db.getPostByUser(user)
    return render_template('perfil.html', usuario=dbUser, output=output, auth=auth)
  else:
    output = db.getPostByUser(user)
    dbUser2 = db.getUser(user)
    if dbUser2['User'] == user:
      usr = True
    return render_template('perfil.html', usuario=dbUser, output=output, auth=auth, res=dbUser2)

@app.route('/mensajes/<user>', methods=('GET', 'POST'))
def busqueda_msg(user):
  usr = []
  if user == session['usuario']:
    dbUser = db.getUser(session['usuario'])
    return render_template('mensajes.html', usuario=dbUser)
  # return render_template('')

@app.route('/busqueda/<user>', methods=("GET", "POST"))
def busqueda(user):
  usr = []
  if user == session['usuario']:
    dbUser = db.getUser(user)
    if dbUser['User'] == user:
      usr = True
    if request.method == 'POST':
      resultado = request.form['busqueda']
      respuesta = db.getUsersByName(resultado)
      print(respuesta)
      return render_template('busqueda.html', usuario=dbUser, respuestas=respuesta)
  else:
    return render_template('busqueda.html', usuario=usr)
  # return render_template('')

@app.route('/amigos/')
def amigo():
  return redirect('/feed/<session["usuario"]>')

@app.route('/amigos/<user>')
def amigos(user):
  usr = []
  if user == session['usuario']:
    dbUser = db.getUser(session['usuario'])
    if request.method == 'GET':
      resultado = db.getUsers()
      return render_template('amigos.html', usuario=dbUser, respuestas=resultado)
  else:
    return redirect('login', usuario=usr)

@app.route('/fotos/<user>', methods=['GET'])
def fotos(user):
  usr = []
  if user == session['usuario']:
    output = db.getPosts()
    dbUser = db.getUser(session['usuario'])
    return render_template('fotos.html', usuario=dbUser, respuestas=output)
  else:
    return redirect('/feed', session['usuario'])

@app.route('/admin/<user>', methods=('GET', 'POST'))
def admin(user):
  dbUser = db.getUser(session['usuario'])
  print(dbUser)
  if user == session['usuario']:
    return render_template('dashboard.html', usuario=dbUser)
  else:
    return redirect('/')

@app.route('/admin-login', methods=('GET', 'POST'))
def admin_login():
  error = ""
  usr = False
  if request.method == 'POST':
    username = request.form['login-email']
    password = request.form['login-password']
    dbUser = db.getUser(username)
    if dbUser['User'] == username and dbUser['passwrd'] == password:
      usr = True
    if usr:
      session["usuario"] = username
      return redirect('admin/'+session["usuario"])
    else:
      error = "usuario o clave invalidos"
      flash(error, 'error')
      return render_template('admin-login.html');
  else:
    flash("Por favor iniciar sesion", 'error')
    return render_template('admin-login.html');


@app.route('/admin/users', methods=('GET', 'POST'))
def admin_users():
  dbUser = db.getUser(session['usuario'])
  if session['usuario']:
    usuarios = db.getUsers()
    print(usuarios)
    return render_template('dashboard-users.html', usuario=dbUser, usuarios=usuarios)

@app.route('/admin/superusers', methods=('GET', 'POST'))
def admin_superusers():
  dbUser = db.getUser(session['usuario'])
  if session['usuario']:
    usuarios = db.getSuperUsers()
    print(usuarios)
    return render_template('dashboard-superuser.html', usuario=dbUser, usuarios=usuarios)

@app.route("/logout")
def logout():
  session['usuario'] = None
  return redirect("/")
# @app.before_request
# def antes_de_cada_peticion():
#     ruta = request.path
#     # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
#     if not 'usuario' in session and ruta != "/" and ruta != "/logout" and not ruta.startswith("/static"):
#         flash("Inicia sesión para continuar")
#         return redirect("/")
#     # Si ya ha iniciado, no hacemos nada, es decir lo dejamos pasar

# Main
if __name__=='__main__':
    app.run(debug=True, port=5500)
