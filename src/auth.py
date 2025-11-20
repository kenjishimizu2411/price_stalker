import bcrypt

def hash_password(password):
    """Transforma senha texto puro em hash seguro"""
    # O bcrypt precisa de bytes, então usamos .encode()
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8') # Retorna como string para salvar no banco

def check_password(plain_password, hashed_password):
    """Confere se a senha bate com o hash"""
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)