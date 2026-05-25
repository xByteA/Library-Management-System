from sqlalchemy.orm import Session
from models.book import Book


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_book(self, title: str, author: str, isbn: str, genre: str = None, 
                    description: str = None, cover_image_url: str = None, total_copies: int = 1) -> Book:
        """Create a new book"""
        new_book = Book(
            title=title,
            author=author,
            isbn=isbn,
            genre=genre,
            description=description,
            cover_image_url=cover_image_url,
            total_copies=total_copies,
            available_copies=total_copies
        )
        self.db.add(new_book)
        self.db.commit()
        self.db.refresh(new_book)
        return new_book

    def get_book_by_id(self, book_id: str) -> Book:
        """Get book by ID"""
        return self.db.query(Book).filter(Book.id == book_id).first()

    def get_book_by_isbn(self, isbn: str) -> Book:
        """Get book by ISBN"""
        return self.db.query(Book).filter(Book.isbn == isbn).first()

    def delete_book(self, book: Book) -> bool:
        """Delete a book"""
        try:
            self.db.delete(book)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def get_all_books(self):
        """Get all active books"""
        return self.db.query(Book).filter(Book.is_active == True).all()
