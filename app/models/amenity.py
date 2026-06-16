from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, Optional, Literal
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class AmenityBase(BaseModel):
    name: str
    product_type: Literal['all', 'apartment', 'villa', 'townhouse', 'shophouse'] = 'all'
    icon: Optional[str] = None
    is_active: bool = True

class AmenityCreate(AmenityBase):
    pass

class AmenityResponse(AmenityBase):
    id: Optional[PyObjectId] = Field(validation_alias="_id", serialization_alias="id", default=None)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "60a7f1b9b1a2c3d4e5f6g7h8",
                "name": "Bể bơi vô cực",
                "product_type": "apartment",
                "is_active": True
            }
        }
    }
