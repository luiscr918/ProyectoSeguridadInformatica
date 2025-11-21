import gnupg
import os

# Si Kleopatra/GnuPG está instalado, normalmente esta ruta funciona
gpg = gnupg.GPG()

def generar_claves_pgp(nombre: str, correo: str, passphrase: str):
    """
    Genera claves PGP reales compatibles con Kleopatra.
    """

    input_data = gpg.gen_key_input(
        name_real=nombre,
        name_email=correo,
        passphrase=passphrase,
        key_type="RSA",
        key_length=2048
    )

    key = gpg.gen_key(input_data)

    if not key:
        raise Exception("No se pudieron generar las claves PGP.")

    return key.fingerprint


def guardar_clave_publica(fingerprint: str, ruta: str):
    public_key = gpg.export_keys(fingerprint)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(public_key)


def guardar_clave_privada(fingerprint: str, ruta: str, passphrase: str):
    private_key = gpg.export_keys(fingerprint, secret=True, passphrase=passphrase)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(private_key)
