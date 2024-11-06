import hashlib

def encriptar_contraseña(contraseña):
    # Encriptar usando SHA-256
    return hashlib.sha256(contraseña.encode()).hexdigest()
