from pydantic import BaseModel
from typing import Optional


class AddBookRequest(BaseModel):
    title: str
    author: str
    isbn: str
    genre: Optional[str] = None
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    total_copies: int = 1


class DeleteBookRequest(BaseModel):
    id: str
