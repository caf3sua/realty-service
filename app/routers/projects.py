from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.database import get_db, parse_id
from app.models.project import ProjectResponse, ProjectCreate

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.get("", response_model=List[ProjectResponse])
async def get_projects(db=Depends(get_db)):
    """Fetch all projects from the database."""
    projects = []
    cursor = db["realty_projects"].find({})
    async for document in cursor:
        projects.append(document)
    return projects

@router.get("/{slug}", response_model=ProjectResponse)
async def get_project_by_slug(slug: str, db=Depends(get_db)):
    """Fetch a single project by its slug."""
    project = await db["realty_projects"].find_one({"slug": slug})
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
    result = await db["realty_projects"].insert_one(project_dict)
    project_dict["_id"] = result.inserted_id
    return project_dict

@router.put("/{id}", response_model=ProjectResponse)
async def update_project(id: str, project: ProjectCreate, db=Depends(get_db)):
    """Update an existing project by its ID."""
    project_dict = project.model_dump()
    result = await db["realty_projects"].find_one_and_replace({"_id": parse_id(id)}, project_dict)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{id}' not found"
        )
    project_dict["_id"] = id
    return project_dict

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(id: str, db=Depends(get_db)):
    """Delete a project by its ID."""
    result = await db["realty_projects"].delete_one({"_id": parse_id(id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{id}' not found"
        )
    return None

