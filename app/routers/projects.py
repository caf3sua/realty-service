from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.database import get_db
from app.models.project import ProjectResponse, ProjectCreate

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.get("", response_model=List[ProjectResponse])
async def get_projects(db=Depends(get_db)):
    """Fetch all projects from the database."""
    projects = []
    cursor = db["projects"].find({})
    async for document in cursor:
        projects.append(document)
    return projects

@router.get("/{slug}", response_model=ProjectResponse)
async def get_project_by_slug(slug: str, db=Depends(get_db)):
    """Fetch a single project by its slug name."""
    project = await db["projects"].find_one({"slug": slug})
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with slug '{slug}' not found"
        )
    return project

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, db=Depends(get_db)):
    """Create a new project."""
    project_dict = project.model_dump()
    result = await db["projects"].insert_one(project_dict)
    project_dict["_id"] = result.inserted_id
    return project_dict
