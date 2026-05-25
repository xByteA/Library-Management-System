from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.book import AddBookRequest, DeleteBookRequest
from DB.connection import get_db
from repository.book_repository import BookRepository
from services.book_service import BookService
from controllers.book_controller import BookController


bookRouter = APIRouter(tags=["Book"], prefix="/books")


def get_book_controller(db: Session):
    repo = BookRepository(db)
    service = BookService(repo)
    return BookController(service)


# -------- ADD BOOK --------
@bookRouter.post("/add")
def add_book(
    data: AddBookRequest,
    db: Session = Depends(get_db)):
    controller = get_book_controller(db)
    return controller.add_book(data)


# -------- DELETE BOOK --------
@bookRouter.delete("/delete")
def delete_book(
    data: DeleteBookRequest,
    db: Session = Depends(get_db)):
    controller = get_book_controller(db)
    return controller.delete_book(data)
