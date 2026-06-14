import bcrypt
from app.modules.auth.application.ports.output.password_hasher_port import PasswordHasherPort

class BcryptPasswordHasher(PasswordHasherPort):
    def hash(self, password: str) -> str:
        # bcrypt requires bytes
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
        # Store as string in the database
        return hashed_bytes.decode('utf-8')
    
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)