


class AuthController:

    def __init__(self, service):
        self.service = service

    def login(self, data):
        return self.service.login(data)
    
    def register(self, data):
        return self.service.register(data)
    
    def deleteUser(self, data):
        return self.service.deleteUser(data)
    
    def getUserById(self, user_id: str):
        return self.service.getUserById(user_id)