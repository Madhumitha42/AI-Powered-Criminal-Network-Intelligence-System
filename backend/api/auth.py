from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Fictional SIH demo users
DEMO_USERS = {
    "investigator": {"password": "password123", "role": "INVESTIGATOR"},
    "analyst": {"password": "password123", "role": "ANALYST"},
    "admin": {"password": "admin123", "role": "ADMIN"}
}

@router.post("/login", response_model=UserResponse)
def login(credentials: UserLogin):
    user = DEMO_USERS.get(credentials.username.lower())
    if not user or user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    return UserResponse(
        username=credentials.username,
        role=user["role"],
        token=f"demo-jwt-token-{credentials.username}"
    )
