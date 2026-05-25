from repositories.user_repository import UserRepository
from utils.errors.appException import AppException
from schemas.auth import RegisterRequest, LoginRequest, DeleteUserReguest


class AuthService:

    def __init__(self, repo: UserRepository, hashing, token):
        self.repo = repo
        self.hashing = hashing
        self.token = token

    # ---------------- LOGIN ----------------
    def login(self, data: LoginRequest) -> dict:

        user = self.repo.getByEmail(data.email)

        if not user:
            raise AppException("Invalid credentials", 401)

        is_valid = self.hashing.verify(
            data.password,
            user.hashed_password
        )

        if not is_valid:
            raise AppException("Invalid credentials", 401)

        access_token = self.token.encode(
            {
                "id": str(user.id),
                "email": user.email,
                "type": "access"
            }
        )

        refresh_token = self.token.encode(
            {
                "id": str(user.id),
                "type": "refresh"
            }
        )

        return {
            "accessToken": access_token,
            "refreshToken": refresh_token
        }

    # ---------------- REGISTER ----------------
    def register(self, data: RegisterRequest) -> dict:

        user = self.repo.getByEmail(data.email)

        if user:
            raise AppException("User already exists", 409)

        hashed_password = self.hashing.hash(data.password)

        new_user = self.repo.createUser(
            email=data.email,
            full_name=data.full_name,
            password=hashed_password
        )

        return {
            "message": "User created successfully",
            "user": new_user
        }
    
    # ---------------- DELETE USER ----------------
    def deleteUser(self, data: DeleteUserReguest):
        # Decode token to get current user info
        try:
            token_payload = self.token.decode(data.token)
        except ValueError as e:
            raise AppException(str(e), 401)
        
        user_id = token_payload.get("id")        
        user = self.repo.getUserById(data.id)
        if not user:
            raise AppException("User not found", 404)
        
        current_user = self.repo.getUserById(user_id)
        if not current_user:
            raise AppException("Unauthorized", 401)
        
        # Authorization logic
        account_id = str(current_user.id) == data.id
        is_admin = current_user.is_admin()
        
        if account_id and not is_admin:
            pass
        elif is_admin and not user.is_admin():
            pass
        else:
            raise AppException("You don't have permission to delete this account", 403)
        
        # Delete the user
        delete = self.repo.deleteuser(user)
        if not delete:
            raise AppException("Cannot delete user", 500)
        
        return {
            "success": True,
            "message": "Account deleted successfully"
        }
    
    # ---------------- GET USER BY ID ----------------
    def getUserById(self, user_id: str) -> dict:
        user = self.repo.getUserById(user_id)
        if not user:
            raise AppException("User not found", 404)
        
        return {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }