from pydantic import BaseModel
from typing import Optional


class BorrowBookRequest(BaseModel):
    user_id: str
    book_id: str


class ReturnBookRequest(BaseModel):
    borrow_id: str


class PayFineRequest(BaseModel):
    borrow_id: str
