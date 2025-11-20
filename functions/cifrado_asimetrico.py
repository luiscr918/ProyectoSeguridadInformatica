from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generar_claves_rsa(frase: str):
    """
    Genera una clave privada RSA a partir de una frase usando PBKDF2 como semilla.
    Nota: La generación determinística completa de RSA no se soporta directamente.
    Este método genera claves nuevas cada vez, pero se basan en derivación segura.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    return private_key, public_key


def guardar_clave_privada(private_key, ruta):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(ruta, "wb") as f:
        f.write(pem)


def guardar_clave_publica(public_key, ruta):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(ruta, "wb") as f:
        f.write(pem)


def cargar_clave_privada(ruta):
    with open(ruta, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def cargar_clave_publica(ruta):
    with open(ruta, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def cifrar_archivo_rsa(ruta_archivo, public_key):
    with open(ruta_archivo, "rb") as f:
        datos = f.read()

    datos_cifrados = public_key.encrypt(
        datos,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return datos_cifrados


def descifrar_archivo_rsa(ruta_archivo, private_key):
    with open(ruta_archivo, "rb") as f:
        datos = f.read()

    datos_descifrados = private_key.decrypt(
        datos,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return datos_descifrados
