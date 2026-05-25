from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from DB.connection import Base, engine
from routes.book import bookRouter
from utils.errors.appException import AppException


# Create DB tables (with error handling)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Service")

app.include_router(bookRouter)


# Global error handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message
        }
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "book-service"
    }
