from abc import ABC, abstractmethod

class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, plainText: str) -> str:
        pass

    @abstractmethod
    def verify(self, plainText: str, hashed: str) -> bool:
        pass
