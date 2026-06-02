from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_db
from app.models.user import UserLogin, TokenResponse
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db = Depends(get_db)):
    """Authenticate user credentials and return a signed access token and user info."""
    user = await db["realty_users"].find_one({"email": credentials.email.lower()})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu không chính xác"
        )
        
    if not verify_password(credentials.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu không chính xác"
        )
        
    if user.get("status") != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị khóa hoặc ngừng hoạt động"
        )
        
    # Generate token
    token_data = {
        "email": user["email"],
        "role": user["role"]
    }
    token = create_access_token(token_data)
    
    return {"token": token, "user": user}
