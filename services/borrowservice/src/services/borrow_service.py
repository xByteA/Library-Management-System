from repository.borrow_repository import BorrowRepository
from schemas.borrow import BorrowBookRequest, ReturnBookRequest, PayFineRequest
from services.service_clients import UserServiceClient, BookServiceClient
from utils.errors.appException import AppException
from datetime import datetime, timezone, timedelta

# Configuration
MAX_BOOKS_PER_USER = 3
BORROW_DURATION_DAYS = 14
FINE_PER_DAY = 1.0


class BorrowService:
    def __init__(self, repo: BorrowRepository):
        self.repo = repo
        self.user_client = UserServiceClient()
        self.book_client = BookServiceClient()
    
    async def borrow_book(self, data: BorrowBookRequest) -> dict:
        # 1. Validate user exists
        user = await self.user_client.get_user(data.user_id)
        if not user:
            raise AppException("User not found", 404)
        
        # 2. Validate book exists
        book = await self.book_client.get_book(data.book_id)
        if not book:
            raise AppException("Book not found", 404)
        
        # 3. Check if book has available copies
        if book.get("available_copies", 0) <= 0:
            raise AppException("Book is not available for borrowing", 400)
        
        # 4. Check user's active borrows
        active_borrows = self.repo.get_active_borrows_by_user(data.user_id)
        if len(active_borrows) >= MAX_BOOKS_PER_USER:
            raise AppException(
                f"User cannot borrow more than {MAX_BOOKS_PER_USER} books",
                400
            )
        
        # 5. Check if user has unpaid fines
        unpaid_fines = self.repo.get_user_books_with_unpaid_fines(data.user_id)
        if unpaid_fines:
            raise AppException("User has unpaid fines and cannot borrow books", 400)
        
        # 6. Prevent borrowing the same active book twice
        existing_borrow = self.repo.check_user_borrowed_book(data.user_id, data.book_id)
        if existing_borrow:
            raise AppException("User has already borrowed this book", 400)
        
        # 7. Calculate due date
        due_date = datetime.now(timezone.utc) + timedelta(days=BORROW_DURATION_DAYS)
        
        # 8. Create borrow record
        borrow = self.repo.create_borrow(data.user_id, data.book_id, due_date)
        
        # 9. Reduce available copies in Book Service
        await self.book_client.reduce_available_copies(data.book_id)
        
        return {
            "success": True,
            "message": "Book borrowed successfully",
            "borrow": {
                "id": str(borrow.id),
                "user_id": str(borrow.user_id),
                "book_id": str(borrow.book_id),
                "borrowed_at": borrow.borrowed_at.isoformat(),
                "due_date": borrow.due_date.isoformat(),
                "status": borrow.status
            }
        }
    
    async def return_book(self, data: ReturnBookRequest) -> dict:
        """Return a borrowed book"""
        # 1. Validate borrow exists
        borrow = self.repo.get_borrow_by_id(data.borrow_id)
        if not borrow:
            raise AppException("Borrow record not found", 404)
        
        # 2. Prevent returning a book that was never borrowed
        if borrow.status != "active":
            raise AppException("Cannot return a book that is not active", 400)
        
        # 3. Calculate late return fine
        fine_amount = 0.0
        if datetime.now(timezone.utc) > borrow.due_date:
            delayed_days = (
                datetime.now(timezone.utc) - borrow.due_date
            ).days
            if delayed_days > 0:
                fine_amount = delayed_days * FINE_PER_DAY
        
        # 4. Update borrow record
        borrow = self.repo.update_borrow_return(borrow, fine_amount)
        
        # 5. Increase available copies in Book Service
        await self.book_client.increase_available_copies(data.borrow_id)
        
        return {
            "success": True,
            "message": "Book returned successfully",
            "borrow": {
                "id": str(borrow.id),
                "returned_at": borrow.returned_at.isoformat(),
                "status": borrow.status,
                "fine_amount": borrow.fine_amount,
                "fine_paid": borrow.fine_paid
            }
        }
    
    async def pay_fine(self, data: PayFineRequest) -> dict:
        # Validate borrow exists
        borrow = self.repo.get_borrow_by_id(data.borrow_id)
        if not borrow:
            raise AppException("Borrow record not found", 404)
        
        # Check if fine exists
        if borrow.fine_amount <= 0:
            raise AppException("No fine to pay for this borrow", 400)
        
        # Mark fine as paid
        borrow = self.repo.update_fine_paid(borrow)
        
        return {
            "success": True,
            "message": "Fine paid successfully",
            "borrow": {
                "id": str(borrow.id),
                "fine_amount": borrow.fine_amount,
                "fine_paid": borrow.fine_paid
            }
        }