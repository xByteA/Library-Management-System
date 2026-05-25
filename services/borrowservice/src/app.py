from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from DB.connection import Base, engine
from routes.borrow import borrowRouter
from utils.errors.appException import AppException


# Create DB tables (with error handling)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not create database tables: {e}")

app = FastAPI(title="Borrow Service")

app.include_router(borrowRouter)


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
        "service": "borrow-service"
    }
