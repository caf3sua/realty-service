import random
import string
import re
import unicodedata
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.database import get_db, parse_id
from app.models.post import PostResponse, PostCreate

router = APIRouter(prefix="/api/posts", tags=["Posts"])

def slugify(text: str) -> str:
    # Normalize to decompose accents (NFD)
    text = unicodedata.normalize('NFD', text)
    # Filter out accents
    text = "".join([c for c in text if not unicodedata.combining(c)])
    # Convert 'đ' / 'Đ' to 'd'
    text = text.replace('đ', 'd').replace('Đ', 'd')
    # Lowercase
    text = text.lower()
    # Remove non-alphanumeric characters except spaces and hyphens
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    # Replace spaces and multiple hyphens with single hyphen
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def generate_random_suffix(length: int = 5) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

@router.get("", response_model=List[PostResponse])
async def get_posts(db=Depends(get_db)):
    """Fetch all posts from the database."""
    posts = []
    cursor = db["realty_posts"].find({})
    async for document in cursor:
        posts.append(document)
    return posts

@router.get("/{slug}", response_model=PostResponse)
async def get_post_by_slug(slug: str, db=Depends(get_db)):
    """Fetch a single post by its slug."""
    post = await db["realty_posts"].find_one({"slug": slug})
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with slug '{slug}' not found"
        )
    return post

@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db=Depends(get_db)):
    """Create a new post with generated unique slug."""
    post_dict = post.model_dump()
    
    # Generate slug with random suffix to ensure uniqueness
    base_slug = post_dict.get("slug") or slugify(post_dict["title"])
    cleaned_base = slugify(base_slug)
    suffix = generate_random_suffix()
    post_dict["slug"] = f"{cleaned_base}-{suffix}"
    
    result = await db["realty_posts"].insert_one(post_dict)
    post_dict["_id"] = result.inserted_id
    return post_dict

@router.put("/{id}", response_model=PostResponse)
async def update_post(id: str, post: PostCreate, db=Depends(get_db)):
    """Update an existing post."""
    post_dict = post.model_dump()
    # Note: For updates, we replace the document and preserve the slug passed by the client.
    result = await db["realty_posts"].find_one_and_replace({"_id": parse_id(id)}, post_dict)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID '{id}' not found"
        )
    post_dict["_id"] = id
    return post_dict

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: str, db=Depends(get_db)):
    """Delete a post by its ID."""
    result = await db["realty_posts"].delete_one({"_id": parse_id(id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID '{id}' not found"
        )
    return None
