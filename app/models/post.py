from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, Optional, Literal

# Custom type to handle MongoDB ObjectIds as string representation in JSON output
PyObjectId = Annotated[str, BeforeValidator(str)]

class PostBase(BaseModel):
    title: str
    slug: str
    summary: str
    content: str
    image: str
    category: Literal['Thị trường', 'Quy hoạch', 'Cẩm nang', 'Dự án']
    publishedAt: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: Optional[PyObjectId] = Field(validation_alias="_id", serialization_alias="id", default=None)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "60c72b2f9b1d8e234c8f4b5a",
                "title": "Bất Động Sản Ven Biển Quảng Ninh Bứt Phá Nhờ Đòn Bẩy Hạ Tầng",
                "slug": "bat-dong-san-ven-bien-quang-ninh-but-pha-ha-tang-a8f3b",
                "summary": "Với việc hoàn thiện các tuyến cao tốc...",
                "content": "<p>Thị trường bất động sản Quảng Ninh...</p>",
                "image": "/images/ha-long-xanh-hero.png",
                "category": "Thị trường",
                "publishedAt": "2026-05-25"
            }
        }
    }
