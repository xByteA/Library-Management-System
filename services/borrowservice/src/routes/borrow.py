from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.borrow import BorrowBookRequest, ReturnBookRequest, PayFineRequest
from DB.connection import get_db
from repository.borrow_repository import BorrowRepository
from services.borrow_service import BorrowService
from controllers.borrow_controller import BorrowController


borrowRouter = APIRouter(tags=["Borrow"], prefix="/borrow")


def get_borrow_controller(db: Session):
    repo = BorrowRepository(db)
    service = BorrowService(repo)
    return BorrowController(service)


# -------- BORROW BOOK --------
@borrowRouter.post("/")
async def borrow_book(
    data: BorrowBookRequest,
    db: Session = Depends(get_db)):
    controller = get_borrow_controller(db)
    return await controller.borrow_book(data)


# -------- RETURN BOOK --------
@borrowRouter.post("/return/{borrow_id}")
async def return_book(
    borrow_id: str,
    db: Session = Depends(get_db)):
    data = ReturnBookRequest(borrow_id=borrow_id)
    controller = get_borrow_controller(db)
    return await controller.return_book(data)


# -------- PAY FINE --------
@borrowRouter.post("/pay-fine/{borrow_id}")
async def pay_fine(
    borrow_id: str,
    db: Session = Depends(get_db)):
    data = PayFineRequest(borrow_id=borrow_id)
    controller = get_borrow_controller(db)
    return await controller.pay_fine(data)
