"""Aqui estan todos los metodos para poder encriptar"""

from cryptography.fernet import Fernet


def generar_clave():
    """
    Genera y devuelve una clave Fernet(AES 128 en CBS + HMAC)
    """
    return Fernet.generate_key()


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
    datos_cifrados = fernet.encrypt(datos)
    return datos_cifrados


def descifrar_archivo(ruta_archivo, clave):
    """
    Recibe la ruta del archivo cifrado y la clave
    Devuleve los bytes descifrados
    """
    fernet = Fernet(clave)

    with open(ruta_archivo, "rb") as f:
        datos = f.read()

    datos_descifrados = fernet.decrypt(datos)
    return datos_descifrados
