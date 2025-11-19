"""Aqui estan todos los metodos para poder encriptar"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64 
import os

def clave_desde_password(password:str,salt:bytes)-> bytes:
    """
    Deriva una clave Fernet válida desde una contraseña escrita por el usuario
    """
    kdf= PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, #tamaño requerido por Fernet
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64decode(kdf.derive(password.encode()))


def cifrar_archivo(ruta_archivo, clave):
    """
    Recive la ruta del archivo original y la clave fernet
    Devuelve los bytes cifrados
    """
    fernet = Fernet(clave)

    # leer datos
    with open(ruta_archivo, "rb") as f:
        datos = f.read()

    # cifrar
    return fernet.encrypt(datos)


def descifrar_archivo(ruta_archivo, clave):
    """
    Recibe la ruta del archivo cifrado y la clave
    Devuleve los bytes descifrados
    """
    fernet = Fernet(clave)

    with open(ruta_archivo, "rb") as f:
        datos = f.read()

    return fernet.decrypt(datos)
