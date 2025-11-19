"""functions/cifrado_simetrico.py"""

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def clave_desde_password(password: str, salt: bytes) -> bytes:
    """
    Deriva una clave Fernet válida desde una contraseña escrita por el usuario.
    Devuelve la clave codificada en base64 URL-safe (requerido por Fernet).
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # tamaño requerido por Fernet
        salt=salt,
        iterations=390000,
    )
    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)


def cifrar_archivo(ruta_archivo, clave_fernet: bytes) -> bytes:
    """
    Recibe la ruta del archivo original y la clave fernet (base64 urlsafe bytes).
    Devuelve los bytes cifrados.
    """
    fernet = Fernet(clave_fernet)
    with open(ruta_archivo, "rb") as f:
        datos = f.read()
    return fernet.encrypt(datos)


def descifrar_archivo_bytes(datos_cifrados: bytes, clave_fernet: bytes) -> bytes:
    """
    Descifra bytes ya leídos y devuelve los bytes descifrados.
    (Útil cuando hemos separado salt + datos)
    """
    fernet = Fernet(clave_fernet)
    return fernet.decrypt(datos_cifrados)
