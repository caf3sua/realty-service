from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, Optional, List, Literal

PyObjectId = Annotated[str, BeforeValidator(str)]

class ProjectBase(BaseModel):
    name: str
    slug: str
    location: str
    developer: str
    description: str
    shortDescription: str
    image: str
    banner: str
    status: Literal['Đang mở bán', 'Sắp mở bán', 'Đã bàn giao']
    scale: str
    priceRange: str
    tags: List[str]

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "60c72b2f9b1d8e234c8f4b5b",
                "name": "Vinhomes Ocean Park 1",
                "slug": "ocean-park-1",
                "location": "Gia Lâm, Hà Nội",
                "developer": "Vinhomes",
                "description": "Vinhomes Ocean Park 1 sở hữu đại tiện ích độc đáo...",
                "shortDescription": "Thành phố Biển hồ - Nơi mang biển xanh cát trắng...",
                "image": "/images/project-op1.png",
                "banner": "/images/project-op1-banner.png",
                "status": "Đã bàn giao",
                "scale": "420 ha",
                "priceRange": "2.5 tỷ - 120 tỷ",
                "tags": ["Biển hồ nhân tạo", "Hồ nước ngọt lớn", "Vinhomes"]
            }
        }
    }
