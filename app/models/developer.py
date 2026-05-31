from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, Optional

# Custom type to handle MongoDB ObjectIds as string representation in JSON output
PyObjectId = Annotated[str, BeforeValidator(str)]

class DeveloperBase(BaseModel):
    name: str
    logo: str
    title: str
    description: str
    slug: str
    linkText: str

class DeveloperCreate(DeveloperBase):
    pass

class DeveloperResponse(DeveloperBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "60c72b2f9b1d8e234c8f4b5a",
                "name": "Masterise Homes",
                "logo": "/images/logo-Masterise-Homes.png",
                "title": "Phong Cách Sống Hàng Hiệu",
                "description": "Nhà phát triển bất động sản hàng hiệu hàng đầu Việt Nam...",
                "slug": "masterise-homes",
                "linkText": "Xem Các Căn Hộ Masterise Homes"
            }
        }
    }
