from sqlalchemy.orm import Session
from models.user import User


class UserRepository:
    def __init__(self, db:Session):
        self.db= db

    def createUser(
        self,
        email: str,
        full_name: str,
        password: str
        ):
        user = User(
            email=email,
            full_name=full_name,
            hashed_password=password
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    

    def getUserById(self, id:str):
        return self.db.query(User).filter(User.id == id).first()

    def getByEmail(self,email:str) -> User:
        return self.db.query(User).filter(User.email==email).first()
    
    def getAll(self):
        return self.db.query(User).all()
    
    def deleteuser(self, data:User):
        self.db.delete(data)
        self.db.commit()
        return True