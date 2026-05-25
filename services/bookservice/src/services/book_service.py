from repository.book_repository import BookRepository
from schemas.book import AddBookRequest, DeleteBookRequest
from utils.errors.appException import AppException


class BookService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def add_book(self, data: AddBookRequest) -> dict:
        # Check if book with same ISBN already exists
        existing_book = self.repo.get_book_by_isbn(data.isbn)
        if existing_book:
            raise AppException("Book with this ISBN already exists", 409)

        # Create new book
        new_book = self.repo.create_book(
            title=data.title,
            author=data.author,
            isbn=data.isbn,
            genre=data.genre,
            description=data.description,
            cover_image_url=data.cover_image_url,
            total_copies=data.total_copies
        )

        return {
            "message": "Book added successfully",
            "book": {
                "id": str(new_book.id),
                "title": new_book.title,
                "author": new_book.author,
                "isbn": new_book.isbn,
                "genre": new_book.genre,
                "total_copies": new_book.total_copies,
                "available_copies": new_book.available_copies
            }
        }

    def delete_book(self, data: DeleteBookRequest) -> dict:
        book = self.repo.get_book_by_id(data.id)
        if not book:
            raise AppException("Book not found", 404)

        # Delete the book
        deleted = self.repo.delete_book(book)
        if not deleted:
            raise AppException("Cannot delete book", 500)

        return {
            "success": True,
            "message": "Book deleted successfully"
        }
