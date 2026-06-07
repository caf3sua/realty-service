from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.database import get_db
from app.models.user import UserLogin, TokenResponse
from app.core.security import verify_password, create_access_token, verify_google_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class GoogleLoginRequest(BaseModel):
    token: str

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

@router.post("/google", response_model=TokenResponse)
async def login_google(credentials: GoogleLoginRequest, db = Depends(get_db)):
    """Authenticate Google ID token and return a signed access token and user info."""
    # Verify google token
    id_info = verify_google_token(credentials.token)
    email = id_info.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token Google không chứa địa chỉ email."
        )
        
    # Find user in DB
    user = await db["realty_users"].find_one({"email": email.lower()})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản Google này chưa được cấp quyền truy cập hệ thống."
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

