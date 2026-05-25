import jwt  # type: ignore
from datetime import datetime, timedelta
from .ITokenProvider import TokenProvider


class PyJWTAdapter(TokenProvider):
    def __init__(self, secret, algorithm="HS256"):
        self.secret = secret
        self.algorithm = algorithm

    def encode(self, payload: dict, expires_in: int = 30*60) -> str:
        payload_copy = payload.copy()
        
        if expires_in is not None:
            payload_copy['exp'] = datetime.utcnow() + timedelta(seconds=expires_in)
        
        return jwt.encode(payload_copy, self.secret, algorithm=self.algorithm)

    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token provided")
