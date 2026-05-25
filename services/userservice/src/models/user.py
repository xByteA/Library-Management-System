import uuid
from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from DB.Connection import Base


class UserRole:
    MEMBER    = "member"
    LIBRARIAN = "librarian"
    ADMIN     = "admin"

    ALL = [MEMBER, LIBRARIAN, ADMIN]


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    email = Column(String(255),unique=True,nullable=False,index=True)
    full_name = Column(String(255),nullable=False)
    hashed_password = Column(String(255),nullable=False)
    role = Column(String(50),nullable=False,default=UserRole.MEMBER)
    is_active = Column(Boolean,nullable=False,default=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def is_librarian(self) -> bool:
        return self.role in (UserRole.LIBRARIAN, UserRole.ADMIN)

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role}>"