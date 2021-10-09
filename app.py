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

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

lista_usuarios = {
  1 : {"user": "jhonTa","nombre" : "Jhon Jairo Tamayo Martinez","passwd" : "abc123", "img" :"https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=580&q=80", "imgdestacada" : "https://images.unsplash.com/photo-1511497584788-876760111969?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1032&q=80", "Pais" : "Colombia"},
  2 : {"user": "simon","nombre" : "Simon Vallejo Valencia","passwd" : "abc123", "img" :"https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=580&q=80", "imgdestacada" : "https://images.unsplash.com/photo-1511497584788-876760111969?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1032&q=80", "Pais" : "Colombia"},
  3 : {"user": "roberto","nombre" : "Jhon Jairo Tamayo Martinez","passwd" : "abc123", "img" :"https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=580&q=80", "imgdestacada" : "https://images.unsplash.com/photo-1511497584788-876760111969?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1032&q=80", "Pais" : "Colombia"},
  4 : {"user": "elpepe","nombre" : "Jhon Jairo Tamayo Martinez","passwd" : "abc123", "img" :"https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=580&q=80", "imgdestacada" : "https://images.unsplash.com/photo-1511497584788-876760111969?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1032&q=80", "Pais" : "Colombia"},
  5 : {"user": "carlos","nombre" : "Juana Lopez", "img" :"https://www.kindpng.com/picc/m/442-4426396_profile-picture-woman-circle-hd-png-download.png", "imgdestacada" : "https://images.unsplash.com/photo-1511497584788-876760111969?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1032&q=80", "Pais" : "Colombia"},
  6 : {"user": "simon","nombre" : "Juana Lopez", "img" :"https://www.kindpng.com/picc/m/442-4426396_profile-picture-woman-circle-hd-png-download.png", "imgdestacada" : "https://images.unsplash.com/photo-1511497584788-876760111969?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1032&q=80", "Pais" : "Colombia"}}

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
    estado= db.addProducto(a , "post", status)
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
    for key, usuario in lista_usuarios.items():
      if usuario['user'] == username and usuario['passwd'] == password:
        usr = True
    if usr:
      session["usuario"] = username
      return redirect('feed/'+username)
    else:
      error = "usuario o clave invalidos"
      flash(error, 'error')
      return render_template('login.html');
  else:
    flash(error, 'error')
    return render_template('login.html');
    
    # return jsonify({"encontrado" : encontrado})

@app.route('/feed/<user>', methods=('GET', 'POST'))
def main_page(user):
  usr = []
  for key, usuario in lista_usuarios.items():
        if usuario['user'] == user:
          usr = usuario
  if usr:
    output = db.getImagenes()
    return render_template('feed.html', usuario=usr, output=output)
  else:
    return redirect('/')

@app.route('/admin-login', methods=('GET', 'POST'))
def login_admin():
  return render_template('login.html', methods=('GET', 'POST'))
  
@app.route('/registro/<usuario>', methods=('GET', 'POST'))
def register(usuario):
  return render_template('login.html', usuario=usuario)

@app.route('/profile/<user>', methods=('GET', 'POST'))
def busqueda2(user):
  usr = []
  for key, usuario in lista_usuarios.items():
        if usuario['user'] == user:
          usr = usuario
  if usr:
    output = db.getImagenes()
    return render_template('feed.html', usuario=usr, output=output)
  else:
    return redirect('/')

@app.route('/admin/<user>', methods=('GET', 'POST'))
def admin_login(user):
  usr = []
  for key, usuario in lista_usuarios.items():
        if usuario['user'] == user:
          usr = usuario
  return render_template('dashboard.html', usuario=usr)


@app.route('/mensajes/<user>', methods=('GET', 'POST'))
def busqueda_msg(user):
  usr = []
  for key, usuario in lista_usuarios.items():
        if usuario['user'] == user:
          usr = usuario
  return render_template('busqueda.html', usuario=usr)
  # return render_template('')

@app.route('/busqueda/<user>', methods=("GET", "POST"))
def busqueda(user):
  usr = []
  for key, usuario in lista_usuarios.items():
        if usuario['user'] == user:
          usr = usuario
  if request.method == 'POST':
    resultado = request.form['busqueda']
    respuesta = []
    for key, busqueda in lista_usuarios.items():
        if busqueda['user'] == resultado:
          respuesta.append(busqueda);
    return render_template('busqueda.html', usuario=usr, respuestas=respuesta)
  else:
    return render_template('busqueda.html', usuario=usr)
  # return render_template('')

@app.before_request
def antes_de_cada_peticion():
    ruta = request.path
    # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
    if not 'usuario' in session and ruta != "/" and ruta != "/logout" and not ruta.startswith("/static"):
        flash("Inicia sesión para continuar")
        return redirect("/")
    # Si ya ha iniciado, no hacemos nada, es decir lo dejamos pasar

# Main
if __name__=='__main__':
    app.run(debug=True, port=4000)
