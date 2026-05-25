from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    accessToken: str
    refreshToken: str

class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class DeleteUserReguest(BaseModel):
    id: str
    token: str

