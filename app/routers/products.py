from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.core.database import get_db, parse_id
from app.models.product import ProductResponse, ProductCreate

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("", response_model=List[ProductResponse])
async def get_products(
    product_type: Optional[str] = None,
    developer: Optional[str] = None,
    is_premium: Optional[bool] = None,
    project_slug: Optional[str] = None,
    db=Depends(get_db)
):
    """Fetch all products with optional filters."""
    query = {}
    if product_type:
        query["productType"] = product_type
    if developer:
        query["developer"] = developer
    if is_premium is not None:
        query["isPremium"] = is_premium
    if project_slug:
        query["projectSlug"] = project_slug

    products = []
    cursor = db["realty_products"].find(query)
    async for document in cursor:
        products.append(document)
    return products

@router.get("/{slug}", response_model=ProductResponse)
async def get_product_by_slug(slug: str, db=Depends(get_db)):
    """Fetch a single product by its slug."""
    product = await db["realty_products"].find_one({"slug": slug})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with slug '{slug}' not found"
        )
    return product

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db=Depends(get_db)):
    """Create a new product."""
    product_dict = product.model_dump()
    # If client passed an id, we can set it as MongoDB _id
    # Otherwise, it will be generated automatically
    result = await db["realty_products"].insert_one(product_dict)
    product_dict["_id"] = result.inserted_id
    return product_dict

@router.put("/{id}", response_model=ProductResponse)
async def update_product(id: str, product: ProductCreate, db=Depends(get_db)):
    """Update an existing product."""
    product_dict = product.model_dump()
    result = await db["realty_products"].find_one_and_replace({"_id": parse_id(id)}, product_dict)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )
    product_dict["_id"] = id
    return product_dict

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str, db=Depends(get_db)):
    """Delete a product by its ID."""
    result = await db["realty_products"].delete_one({"_id": parse_id(id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{id}' not found"
        )
    return None
