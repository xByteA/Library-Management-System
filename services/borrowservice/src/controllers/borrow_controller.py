from services.borrow_service import BorrowService


class BorrowController:
    def __init__(self, service: BorrowService):
        self.service = service
    
    async def borrow_book(self, data):
        return await self.service.borrow_book(data)
    
    async def return_book(self, data):
        return await self.service.return_book(data)
    
    async def pay_fine(self, data):
        return await self.service.pay_fine(data)
