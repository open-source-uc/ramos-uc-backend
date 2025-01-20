import bcrypt
import hashlib

def encriptar_password(password: str):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
    return hashed.decode('utf-8')

def validacion_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def hash_text(text: str) -> str:
    """
    Hashea el texto usando SHA-256 y devuelve el hash en formato hexadecimal.
    
    :param text: El texto que se quiere hashear
    :return: El hash SHA-256 en formato hexadecimal
    """
    # Crear un objeto hash SHA-256
    hash_object = hashlib.sha256()
    
    # Actualizar el objeto hash con el texto (convertido a bytes)
    hash_object.update(text.encode('utf-8'))
    
    # Obtener el hash en formato hexadecimal
    return hash_object.hexdigest()