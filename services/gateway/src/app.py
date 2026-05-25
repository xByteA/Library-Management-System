import os

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response

BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL", "http://localhost:3002")
BORROW_SERVICE_URL = os.getenv("BORROW_SERVICE_URL", "http://localhost:3003")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:3001")

app = FastAPI(title="API Gateway")


async def proxy_request(request: Request, url: str) -> Response:
    headers = {k: v for k, v in request.headers.items() if k not in {"host", "content-length"}}
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            params=request.query_params,
            content=await request.body(),
            timeout=10.0,
        )

    if response.is_error:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type"),
    )


@app.get("/health")
async def health():
    async with httpx.AsyncClient(timeout=5.0) as client:
        statuses = {}
        for name, url in (
            ("book_service", f"{BOOK_SERVICE_URL}/health"),
            ("borrow_service", f"{BORROW_SERVICE_URL}/health"),
            ("user_service", f"{USER_SERVICE_URL}/health"),
        ):
            try:
                response = await client.get(url)
                statuses[name] = {
                    "status_code": response.status_code,
                    "healthy": response.status_code == 200,
                    "detail": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                }
            except Exception as exc:
                statuses[name] = {"status_code": None, "healthy": False, "detail": str(exc)}

    return {
        "status": "ok",
        "gateway": "running",
        "services": statuses,
    }


@app.api_route("/api/books/add", methods=["POST"])
async def add_book(request: Request):
    return await proxy_request(request, f"{BOOK_SERVICE_URL}/books/add")


@app.api_route("/api/books/delete", methods=["DELETE"])
async def delete_book(request: Request):
    return await proxy_request(request, f"{BOOK_SERVICE_URL}/books/delete")


@app.api_route("/api/borrow", methods=["POST"])
async def borrow_book(request: Request):
    return await proxy_request(request, f"{BORROW_SERVICE_URL}/borrow")


@app.api_route("/api/borrow/return/{borrow_id}", methods=["POST"])
async def return_book(borrow_id: str, request: Request):
    return await proxy_request(request, f"{BORROW_SERVICE_URL}/borrow/return/{borrow_id}")


@app.api_route("/api/borrow/pay-fine/{borrow_id}", methods=["POST"])
async def pay_fine(borrow_id: str, request: Request):
    return await proxy_request(request, f"{BORROW_SERVICE_URL}/borrow/pay-fine/{borrow_id}")


@app.api_route("/api/auth/login", methods=["POST"])
async def login(request: Request):
    return await proxy_request(request, f"{USER_SERVICE_URL}/auth/login")


@app.api_route("/api/auth/register", methods=["POST"])
async def register(request: Request):
    return await proxy_request(request, f"{USER_SERVICE_URL}/auth/register")


@app.api_route("/api/auth/deleteuser", methods=["DELETE"])
async def delete_user(request: Request):
    return await proxy_request(request, f"{USER_SERVICE_URL}/auth/deleteuser")


@app.api_route("/api/auth/{user_id}", methods=["GET"])
async def get_user(user_id: str, request: Request):
    return await proxy_request(request, f"{USER_SERVICE_URL}/auth/{user_id}")
