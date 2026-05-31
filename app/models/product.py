from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, Optional, List, Literal

PyObjectId = Annotated[str, BeforeValidator(str)]

class ProductBase(BaseModel):
    title: str
    slug: str
    price: float
    pricePerSqm: Optional[float] = None
    area: float
    bedrooms: int
    bathrooms: int
    location: str
    description: str
    projectSlug: str
    productType: Literal['villa', 'townhouse', 'apartment', 'residential', 'shophouse']
    productTypeName: str
    isPremium: bool
    developer: Optional[str] = None
    images: List[str]
    status: Literal['Còn hàng', 'Đã cọc', 'Đã bán', 'Đang bán', 'Sắp mở bán']
    direction: str
    legal: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "prod-1",
                "title": "Biệt Thự Đơn Lập Ngọc Trai Siêu VIP - View Trực Diện Biển Hồ Ngọc Trai",
                "slug": "biet-thu-don-lap-ngoc-trai-view-bien-ho",
                "price": 95.0,
                "pricePerSqm": 316.6,
                "area": 300,
                "bedrooms": 5,
                "bathrooms": 6,
                "location": "Phân khu Ngọc Trai, Vinhomes Ocean Park 1",
                "description": "Siêu phẩm biệt thự đơn lập phân khu Ngọc Trai...",
                "projectSlug": "ocean-park-1",
                "productType": "villa",
                "productTypeName": "Biệt thự",
                "isPremium": True,
                "developer": "Vinhomes",
                "images": ["/images/prop-villa-1.png", "/images/prop-villa-1-int.png"],
                "status": "Còn hàng",
                "direction": "Đông Nam",
                "legal": "Sổ đỏ lâu dài"
            }
        }
    }
