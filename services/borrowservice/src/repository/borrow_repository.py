from sqlalchemy.orm import Session
from models.borrow import Borrow, BorrowStatus
from datetime import datetime, timezone, timedelta


class BorrowRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_borrow(self, user_id: str, book_id: str, due_date: datetime) -> Borrow:
        borrow = Borrow(
            user_id=user_id,
            book_id=book_id,
            borrowed_at=datetime.now(timezone.utc),
            due_date=due_date,
            status=BorrowStatus.ACTIVE
        )
        self.db.add(borrow)
        self.db.commit()
        self.db.refresh(borrow)
        return borrow
    
    def get_borrow_by_id(self, borrow_id: str) -> Borrow:
        """Get borrow record by ID"""
        return self.db.query(Borrow).filter(Borrow.id == borrow_id).first()
    
    def get_active_borrows_by_user(self, user_id: str) -> list:
        """Get active borrow records for a user"""
        return self.db.query(Borrow).filter(
            Borrow.user_id == user_id,
            Borrow.status == BorrowStatus.ACTIVE
        ).all()
    
    def get_user_books_with_unpaid_fines(self, user_id: str) -> list:
        """Get borrow records with unpaid fines for a user"""
        return self.db.query(Borrow).filter(
            Borrow.user_id == user_id,
            Borrow.fine_amount > 0,
            Borrow.fine_paid == False
        ).all()
    
    def check_user_borrowed_book(self, user_id: str, book_id: str) -> Borrow:
        """Check if user has already borrowed this book (active)"""
        return self.db.query(Borrow).filter(
            Borrow.user_id == user_id,
            Borrow.book_id == book_id,
            Borrow.status == BorrowStatus.ACTIVE
        ).first()
    
    def update_borrow_return(self, borrow: Borrow, fine_amount: float = 0.0):
        """Update borrow record on return"""
        borrow.returned_at = datetime.now(timezone.utc)
        borrow.status = BorrowStatus.RETURNED
        borrow.fine_amount = fine_amount
        borrow.fine_paid = False if fine_amount > 0 else True
        self.db.commit()
        self.db.refresh(borrow)
        return borrow
    
    def update_fine_paid(self, borrow: Borrow):
        """Mark fine as paid"""
        borrow.fine_paid = True
        borrow.fine_amount = 0.0
        self.db.commit()
        self.db.refresh(borrow)
        return borrow
