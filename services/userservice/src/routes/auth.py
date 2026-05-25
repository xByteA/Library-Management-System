from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.errors.appException import AppException
from schemas.auth import LoginRequest, RegisterRequest, DeleteUserReguest
from DB.Connection import get_db
from repositories.user_repository import UserRepository
from services.auth import AuthService
from controllers.auth import AuthController
from utils.cryptography.bcryptAdapter import BcryptAdapter
from utils.cryptography.pyjwtAdapter import PyJWTAdapter
authRouter= APIRouter(tags=["Auth"], prefix="/auth") 



def get_auth_controller(db: Session):

    repo = UserRepository(db)

    hashing = BcryptAdapter()

    token = PyJWTAdapter("seif123")

    service = AuthService(
        repo,
        hashing,
        token
    )

    return AuthController(service)


# -------- LOGIN --------
@authRouter.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)):

    controller = get_auth_controller(db)
    return controller.login(data)


# -------- REGISTER --------
@authRouter.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)):

    controller = get_auth_controller(db)
    return controller.register(data)


# -------- DELETE USER --------
@authRouter.delete("/deleteuser")
def deleteuser(
    data: DeleteUserReguest,
    db: Session = Depends(get_db)):

    controller = get_auth_controller(db)
    return controller.deleteUser(data)


# -------- GET USER BY ID --------
@authRouter.get("/{user_id}")
def get_user(
    user_id: str,
    db: Session = Depends(get_db)):

    controller = get_auth_controller(db)
    return controller.getUserById(user_id)
