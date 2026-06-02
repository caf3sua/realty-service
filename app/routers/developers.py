from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.database import get_db, parse_id
from app.models.developer import DeveloperResponse, DeveloperCreate

router = APIRouter(prefix="/api/developers", tags=["Developers"])

@router.get("", response_model=List[DeveloperResponse])
async def get_developers(db=Depends(get_db)):
    """Fetch all developers from the database."""
    developers = []
    cursor = db["realty_developers"].find({})
    async for document in cursor:
        developers.append(document)
    return developers

@router.post("", response_model=DeveloperResponse, status_code=status.HTTP_201_CREATED)
async def create_developer(developer: DeveloperCreate, db=Depends(get_db)):
    """Create a new developer."""
    dev_dict = developer.model_dump()
    result = await db["realty_developers"].insert_one(dev_dict)
    dev_dict["_id"] = result.inserted_id
    return dev_dict

@router.get("/{slug}", response_model=DeveloperResponse)
async def get_developer_by_slug(slug: str, db=Depends(get_db)):
    """Fetch a single developer by its slug."""
    developer = await db["realty_developers"].find_one({"slug": slug})
    if not developer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Developer with slug '{slug}' not found"
        )
    return developer

@router.put("/{id}", response_model=DeveloperResponse)
async def update_developer(id: str, developer: DeveloperCreate, db=Depends(get_db)):
    """Update an existing developer."""
    dev_dict = developer.model_dump()
    result = await db["realty_developers"].find_one_and_replace({"_id": parse_id(id)}, dev_dict)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Developer with ID '{id}' not found"
        )
    dev_dict["_id"] = id
    return dev_dict

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_developer(id: str, db=Depends(get_db)):
    """Delete a developer by its ID."""
    result = await db["realty_developers"].delete_one({"_id": parse_id(id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Developer with ID '{id}' not found"
        )
    return None

