import uuid
from sqlalchemy import Column, String, Integer, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from DB.connection import Base


class Book(Base):
    __tablename__ = "books"
    id= Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    title= Column(String(500), nullable=False, index=True)
    author= Column(String(255), nullable=False, index=True)
    isbn= Column(String(20), unique=True, nullable=False, index=True)
    genre= Column(String(100), nullable=True)
    description= Column(Text, nullable=True)
    cover_image_url= Column(String(500), nullable=True)
    total_copies= Column(Integer, nullable=False, default=1)
    available_copies= Column(Integer,nullable=False, default=1)
    is_active= Column(Boolean,default=True,  nullable=False)


    @property
    def is_available(self) -> bool:
        return self.available_copies > 0 and self.is_active

    def __repr__(self):
        return f"<Book '{self.title}' by {self.author} [{self.available_copies}/{self.total_copies}]>"