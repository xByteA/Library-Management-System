from abc import ABC, abstractmethod

class TokenProvider(ABC):
    @abstractmethod
    def encode(self, payload: dict) -> str:
        pass

    @abstractmethod
    def decode(self, token: str) -> dict:
        pass
