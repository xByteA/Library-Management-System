import httpx
from uuid import UUID
from fastapi import HTTPException, status
import os

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://userservice:3001")

TIMEOUT = httpx.Timeout(2.0)  


async def get_user(user_id: UUID) -> dict:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            resp = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
        except httpx.ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="User Service is unreachable",
            )

    if resp.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="User Service returned an unexpected error",
        )

    return resp.json()


async def user_exists(user_id: UUID) -> bool:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            resp = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
            return resp.status_code == 200
        except httpx.ConnectError:
            return False