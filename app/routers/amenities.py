from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db, parse_id
from app.models.amenity import AmenityResponse, AmenityCreate
from app.core.security import get_current_active_user

router = APIRouter(prefix="/api/amenities", tags=["Amenities"])

@router.get("", response_model=List[AmenityResponse])
async def get_amenities(
    product_type: Optional[str] = None,
    db=Depends(get_db)
):
    """Fetch all amenities, optionally filtered by product_type."""
    query = {}
    if product_type:
        query["product_type"] = product_type

    amenities = []
    cursor = db["realty_amenities"].find(query).sort("created_at", -1)
    async for document in cursor:
        amenities.append(document)
    return amenities

@router.post("", response_model=AmenityResponse, status_code=status.HTTP_201_CREATED)
async def create_amenity(amenity: AmenityCreate, db=Depends(get_db), current_user: dict = Depends(get_current_active_user)):
    """Create a new amenity."""
    amenity_dict = amenity.model_dump()
    amenity_dict["created_at"] = datetime.utcnow()
    amenity_dict["updated_at"] = datetime.utcnow()
    
    result = await db["realty_amenities"].insert_one(amenity_dict)
    amenity_dict["_id"] = result.inserted_id
    return amenity_dict

@router.put("/{id}", response_model=AmenityResponse)
async def update_amenity(id: str, amenity: AmenityCreate, db=Depends(get_db), current_user: dict = Depends(get_current_active_user)):
    """Update an existing amenity."""
    amenity_dict = amenity.model_dump()
    amenity_dict["updated_at"] = datetime.utcnow()
    
    # We don't want to overwrite created_at
    update_data = {"$set": amenity_dict}
    
    result = await db["realty_amenities"].find_one_and_update(
        {"_id": parse_id(id)}, 
        update_data,
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Amenity with ID '{id}' not found"
        )
    return result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_amenity(id: str, db=Depends(get_db), current_user: dict = Depends(get_current_active_user)):
    """Delete an amenity by its ID."""
    result = await db["realty_amenities"].delete_one({"_id": parse_id(id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Amenity with ID '{id}' not found"
        )
    return None
