from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timezone
from app.core.database import get_db, parse_id
from app.core.security import get_current_active_user
from app.models.crm import (
    CustomerCreate, CustomerResponse,
    AdvisoryCreate, AdvisoryResponse,
    NewsletterCreate, NewsletterResponse
)

router = APIRouter(prefix="/api/crm", tags=["CRM"])

# Helper to get current ISO time string
def get_current_time_str() -> str:
    # Use timezone-aware local or UTC time
    return datetime.now().astimezone().isoformat()

# ==========================================
# 1. CUSTOMERS ENDPOINTS (QUẢN LÝ KHÁCH HÀNG)
# ==========================================

@router.get("/customers", response_model=List[CustomerResponse])
async def get_customers(
    classification: Optional[str] = None,
    source: Optional[str] = None,
    search: Optional[str] = None,
    db=Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Retrieve all customers with optional filtering and search."""
    query = {}
    if classification:
        query["classification"] = classification
    if source:
        query["source"] = source
    if search:
        # Search by name, phone, or code case-insensitive
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"phone": {"$regex": search, "$options": "i"}},
            {"code": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}}
        ]

    customers = []
    cursor = db["crm_customers"].find(query).sort("createdAt", -1)
    async for document in cursor:
        customers.append(document)
    return customers


@router.get("/customers/{id}", response_model=CustomerResponse)
async def get_customer(
    id: str,
    db=Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Retrieve a single customer by ID."""
    customer = await db["crm_customers"].find_one({"_id": parse_id(id)})
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy khách hàng với ID '{id}'"
        )
    return customer


@router.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_in: CustomerCreate,
    db=Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Create a new customer."""
    # Ensure customer code is unique
    existing_code = await db["crm_customers"].find_one({"code": customer_in.code.strip()})
    if existing_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã khách hàng này đã tồn tại trên hệ thống"
        )

    customer_dict = customer_in.model_dump()
    customer_dict["code"] = customer_dict["code"].strip()
    if customer_dict.get("email"):
        customer_dict["email"] = customer_dict["email"].lower().strip()
    
    if not customer_dict.get("createdAt"):
        customer_dict["createdAt"] = get_current_time_str()

    result = await db["crm_customers"].insert_one(customer_dict)
    customer_dict["_id"] = result.inserted_id
    return customer_dict


@router.put("/customers/{id}", response_model=CustomerResponse)
async def update_customer(
    id: str,
    customer_in: CustomerCreate,
    db=Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Update an existing customer."""
    target_id = parse_id(id)
    customer = await db["crm_customers"].find_one({"_id": target_id})
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy khách hàng với ID '{id}'"
        )

    # Ensure code is unique if changed
    if customer_in.code.strip() != customer.get("code"):
        existing_code = await db["crm_customers"].find_one({"code": customer_in.code.strip()})
        if existing_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mã khách hàng này đã tồn tại trên hệ thống"
            )

    customer_dict = customer_in.model_dump()
    customer_dict["code"] = customer_dict["code"].strip()
    if customer_dict.get("email"):
        customer_dict["email"] = customer_dict["email"].lower().strip()
    
    # Keep the original createdAt
    customer_dict["createdAt"] = customer.get("createdAt", get_current_time_str())

    await db["crm_customers"].replace_one({"_id": target_id}, customer_dict)
    customer_dict["_id"] = target_id
    return customer_dict


@router.delete("/customers/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    id: str,
    db=Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Delete a customer by ID."""
    result = await db["crm_customers"].delete_one({"_id": parse_id(id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy khách hàng với ID '{id}'"
        )
    return None


# ==========================================
# 2. ADVISORY ENDPOINTS (YÊU CẦU TƯ VẤN)
# ==========================================

@router.get("/advisories", response_model=List[AdvisoryResponse])
async def get_advisories(
    status_filter: Optional[str] = None,
    search: Optional[str] = None,
    db=Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Retrieve all advisory requests with optional filtering and search."""
    query = {}
    if status_filter:
        query["status"] = status_filter
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"phone": {"$regex": search, "$options": "i"}},
            {"details": {"$regex": search, "$options": "i"}},
            {"productName": {"$regex": search, "$options": "i"}}
        ]

    advisories = []
    cursor = db["crm_advisories"].find(query).sort("createdAt", -1)
    async for document in cursor:
        advisories.append(document)
    return advisories


@router.get("/advisories/{id}", response_model=AdvisoryResponse)
async def get_advisory(
    id: str,
    db=Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Retrieve a single advisory request by ID."""
    advisory = await db["crm_advisories"].find_one({"_id": parse_id(id)})
    if not advisory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy yêu cầu tư vấn với ID '{id}'"
        )
    return advisory


@router.post("/advisories", response_model=AdvisoryResponse, status_code=status.HTTP_201_CREATED)
async def create_advisory(
    advisory_in: AdvisoryCreate,
    db=Depends(get_db)
):
    """Create a new advisory request. Publicly accessible."""
    advisory_dict = advisory_in.model_dump()
    if not advisory_dict.get("createdAt"):
        advisory_dict["createdAt"] = get_current_time_str()
    if not advisory_dict.get("status"):
        advisory_dict["status"] = "Mới"

    result = await db["crm_advisories"].insert_one(advisory_dict)
    advisory_dict["_id"] = result.inserted_id
    return advisory_dict


@router.put("/advisories/{id}", response_model=AdvisoryResponse)
async def update_advisory_status(
    id: str,
    status_update: str,  # Directly update status via query parameter or request body
    db=Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Update status of an advisory request."""
    target_id = parse_id(id)
    advisory = await db["crm_advisories"].find_one({"_id": target_id})
    if not advisory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy yêu cầu tư vấn với ID '{id}'"
        )

    await db["crm_advisories"].update_one(
        {"_id": target_id},
        {"$set": {"status": status_update}}
    )
    
    advisory["status"] = status_update
    return advisory


@router.delete("/advisories/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_advisory(
    id: str,
    db=Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Delete an advisory request by ID."""
    result = await db["crm_advisories"].delete_one({"_id": parse_id(id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy yêu cầu tư vấn với ID '{id}'"
        )
    return None


# ==========================================
# 3. NEWSLETTER ENDPOINTS (ĐĂNG KÝ NHẬN TIN TỨC)
# ==========================================

@router.get("/newsletters", response_model=List[NewsletterResponse])
async def get_newsletters(
    active: Optional[bool] = None,
    db=Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Retrieve all newsletter subscriptions."""
    query = {}
    if active is not None:
        query["active"] = active

    newsletters = []
    cursor = db["crm_newsletters"].find(query).sort("createdAt", -1)
    async for document in cursor:
        newsletters.append(document)
    return newsletters


@router.post("/newsletters", response_model=NewsletterResponse, status_code=status.HTTP_201_CREATED)
async def subscribe_newsletter(
    newsletter_in: NewsletterCreate,
    db=Depends(get_db)
):
    """Subscribe to newsletter. Publicly accessible."""
    email_clean = newsletter_in.email.lower().strip()
    
    # Check if already subscribed
    existing = await db["crm_newsletters"].find_one({"email": email_clean})
    if existing:
        if not existing.get("active"):
            # Re-activate subscription
            await db["crm_newsletters"].update_one(
                {"_id": existing["_id"]},
                {"$set": {"active": True, "createdAt": get_current_time_str()}}
            )
            existing["active"] = True
            existing["createdAt"] = get_current_time_str()
            return existing
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email này đã đăng ký nhận tin tức từ trước và đang hoạt động"
            )

    newsletter_dict = newsletter_in.model_dump()
    newsletter_dict["email"] = email_clean
    if not newsletter_dict.get("createdAt"):
        newsletter_dict["createdAt"] = get_current_time_str()
    newsletter_dict["active"] = True

    result = await db["crm_newsletters"].insert_one(newsletter_dict)
    newsletter_dict["_id"] = result.inserted_id
    return newsletter_dict


@router.put("/newsletters/{id}", response_model=NewsletterResponse)
async def toggle_newsletter_active(
    id: str,
    active: bool,
    db=Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Toggle the active status of a newsletter subscription."""
    target_id = parse_id(id)
    newsletter = await db["crm_newsletters"].find_one({"_id": target_id})
    if not newsletter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy đăng ký với ID '{id}'"
        )

    await db["crm_newsletters"].update_one(
        {"_id": target_id},
        {"$set": {"active": active}}
    )
    
    newsletter["active"] = active
    return newsletter


@router.delete("/newsletters/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_newsletter(
    id: str,
    db=Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Delete a newsletter subscription by ID."""
    result = await db["crm_newsletters"].delete_one({"_id": parse_id(id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy đăng ký với ID '{id}'"
        )
    return None
