from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.core.database import get_db, parse_id
from app.models.user import UserCreate, UserUpdate, UserResponse
from app.core.security import hash_password, get_current_active_user

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("", response_model=List[UserResponse])
async def get_users(
    role: Optional[str] = None,
    db = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Retrieve all users with optional role filtering."""
    query = {}
    if role:
        query["role"] = role
        
    users = []
    cursor = db["realty_users"].find(query)
    async for document in cursor:
        users.append(document)
    return users

@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(
    id: str,
    db = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Retrieve a single user by ID."""
    user = await db["realty_users"].find_one({"_id": parse_id(id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy người dùng với ID '{id}'"
        )
    return user

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Create a new user with hashed password."""
    # Ensure email is unique
    existing_user = await db["realty_users"].find_one({"email": user_in.email.lower()})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email này đã tồn tại trên hệ thống"
        )
        
    user_dict = user_in.model_dump()
    # Replace plain password with hashed password
    password = user_dict.pop("password")
    user_dict["hashed_password"] = hash_password(password)
    user_dict["email"] = user_dict["email"].lower()
    
    result = await db["realty_users"].insert_one(user_dict)
    user_dict["_id"] = result.inserted_id
    
    return user_dict

@router.put("/{id}", response_model=UserResponse)
async def update_user(
    id: str,
    user_in: UserUpdate,
    db = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Update user details. Hashing password if provided."""
    target_id = parse_id(id)
    
    # Retrieve existing user
    user = await db["realty_users"].find_one({"_id": target_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy người dùng với ID '{id}'"
        )
        
    # Check self-modification restrictions
    is_self = str(current_user["_id"]) == id
    
    user_dict = user_in.model_dump(exclude_unset=True)
    
    # If self-modifying, prevent self-lockout/role changes
    if is_self:
        if "status" in user_dict and user_dict["status"] != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bạn không thể tự khóa tài khoản của chính mình!"
            )
        if "role" in user_dict and user_dict["role"] != current_user["role"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bạn không thể tự thay đổi vai trò quản trị viên của mình!"
            )
            
    # Check email uniqueness if changed
    if "email" in user_dict:
        user_dict["email"] = user_dict["email"].lower()
        if user_dict["email"] != user["email"]:
            existing_email = await db["realty_users"].find_one({"email": user_dict["email"]})
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email này đã tồn tại trên hệ thống"
                )
                
    # Update password if provided
    if "password" in user_dict:
        password = user_dict.pop("password")
        if password.strip():
            user_dict["hashed_password"] = hash_password(password)
        else:
            # If blank password provided, do not update hashed_password
            pass
            
    # Apply changes to MongoDB document
    updated_fields = {**user, **user_dict}
    
    result = await db["realty_users"].find_one_and_replace({"_id": target_id}, updated_fields)
    
    return updated_fields

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: str,
    db = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Delete a user. Prevents deleting oneself."""
    if str(current_user["_id"]) == id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bạn không thể tự xóa tài khoản của chính mình!"
        )
        
    result = await db["realty_users"].delete_one({"_id": parse_id(id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy người dùng với ID '{id}'"
        )
    return None
