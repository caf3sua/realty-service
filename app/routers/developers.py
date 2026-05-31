from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.database import get_db
from app.models.developer import DeveloperResponse, DeveloperCreate

router = APIRouter(prefix="/api/developers", tags=["Developers"])

@router.get("", response_model=List[DeveloperResponse])
async def get_developers(db=Depends(get_db)):
    """Fetch all developers from the database."""
    developers = []
    cursor = db["developers"].find({})
    async for document in cursor:
        developers.append(document)
    return developers

@router.post("", response_model=DeveloperResponse, status_code=status.HTTP_201_CREATED)
async def create_developer(developer: DeveloperCreate, db=Depends(get_db)):
    """Create a new developer."""
    dev_dict = developer.model_dump()
    result = await db["developers"].insert_one(dev_dict)
    dev_dict["_id"] = result.inserted_id
    return dev_dict
