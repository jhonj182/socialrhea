import re
from validate_email import validate_email

pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$"
user_reguex = "^[a-zA-Z0-9_.-]+$"
F_ACTIVE = 'ACTIVE'
F_INACTIVE = 'INACTIVE'
EMAIL_APP = 'EMAIL_APP'
REQ_ACTIVATE = 'REQ_ACTIVATE'
REQ_FORGOT = 'REQ_FORGOT'
U_UNCONFIRMED = 'UNCONFIRMED'
U_CONFIRMED = 'CONFIRMED'

#Validaciones de Email
def isEmailValid(email):
    is_valid = validate_email(email)
    return is_valid

#Vaidaciones de Usuario
def isUsernameValid(user):
    if re.search(user_reguex, user):
        return True
    else:
        return False

#Validaciones de contraseña
def isPasswordValid(password):
    if re.search(pass_reguex, password):
        return True
    else:
        return False
