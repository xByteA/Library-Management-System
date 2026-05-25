import bcrypt
from .IHashing import PasswordHasher

class BcryptAdapter(PasswordHasher):
    def __init__(self, rounds: int = 12):
        self.rounds = rounds
    
    def hash(self, plainText: str) -> str:
        pwd_bytes = plainText.encode('utf-8')
        salt = bcrypt.gensalt(self.rounds)
        hashed = bcrypt.hashpw(pwd_bytes, salt)
        return hashed.decode('utf-8')

    def verify(self, plainText: str, hashed: str) -> bool:
        return bcrypt.checkpw(
            plainText.encode('utf-8'), 
            hashed.encode('utf-8')
        )



