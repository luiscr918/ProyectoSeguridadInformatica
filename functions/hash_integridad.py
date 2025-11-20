import hashlib

def hash_sha256(ruta_archivo):
    sha = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        sha.update(f.read())
    return sha.hexdigest()


def hash_md5(ruta_archivo):
    md5 = hashlib.md5()
    with open(ruta_archivo, "rb") as f:
        md5.update(f.read())
    return md5.hexdigest()


def comparar_hashes(original, copia):
    """
    Retorna True si ambos archivos son idénticos.
    """
    return (
        hash_sha256(original) == hash_sha256(copia) and
        hash_md5(original) == hash_md5(copia)
    )
