from services.book_service import BookService

class BookController:
    def __init__(self, service: BookService):
        self.service = service

    def add_book(self, data):
        return self.service.add_book(data)

    def delete_book(self, data):
        return self.service.delete_book(data)
