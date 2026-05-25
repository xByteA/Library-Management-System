from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from DB.Connection import Base, engine, check_db_connection
from routes.auth import authRouter
from utils.errors.appException import AppException



# create DB taple
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

app.include_router(authRouter)




# glopal error handelar
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message
        }
    )

# check connection database
@app.get("/health")
def health():
    db_ok = check_db_connection()
    return {
        "status": "ok" if db_ok else "degraded",
        "database": "connected" if db_ok else "unreachable",
    }