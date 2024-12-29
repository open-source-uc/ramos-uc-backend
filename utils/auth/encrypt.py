import bcrypt

def encriptar_password(password: str):
    hashed = bcrypt.hashpw(password.enconde('utf-8'), bcrypt.gensalt(20))
    return hashed.decode('utf-8')

def validacion_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))