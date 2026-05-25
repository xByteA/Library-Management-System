import httpx
from typing import Optional, Dict, Any


class UserServiceClient:
    def __init__(self, base_url: str = "http://localhost:3001"):
        self.base_url = base_url
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/auth/{user_id}")
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None


class BookServiceClient:
    def __init__(self, base_url: str = "http://localhost:3002"):
        self.base_url = base_url
    
    async def get_book(self, book_id: str) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/books/{book_id}")
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Error fetching book: {e}")
            return None
    
    async def reduce_available_copies(self, book_id: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.put(
                    f"{self.base_url}/books/{book_id}/reduce-copy"
                )
                return response.status_code == 200
        except Exception as e:
            print(f"Error reducing copies: {e}")
            return False
    
    async def increase_available_copies(self, book_id: str) -> bool:
        """Increase available copies of a book"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.put(
                    f"{self.base_url}/books/{book_id}/increase-copy"
                )
                return response.status_code == 200
        except Exception as e:
            print(f"Error increasing copies: {e}")
            return False
