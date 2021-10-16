import utils

def validarForm(password, rpassword, usuario, email):
  if password != rpassword:
      error = "Las contraseñas son diferentes"
      return error

  if not utils.isUsernameValid(usuario):
    error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
    return error

  if not utils.isPasswordValid(password):
    error = 'La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres'
    return error

  if not utils.isEmailValid(email):
    error = 'Correo invalido'
    return error