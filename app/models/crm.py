from pydantic import BaseModel, Field, BeforeValidator, EmailStr
from typing import Annotated, Optional

# Custom type to handle MongoDB ObjectIds as string representation in JSON output
PyObjectId = Annotated[str, BeforeValidator(str)]

# 1. CUSTOMER MODELS
class CustomerBase(BaseModel):
    name: str
    code: str
    phone: str
    classification: str  # e.g. "Tiềm năng", "Đầu tư", etc.
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    source: str  # e.g. "Facebook", "Website", "Hotline", etc.
    needs: Optional[str] = None
    note: Optional[str] = None
    createdAt: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: Optional[PyObjectId] = Field(validation_alias="_id", serialization_alias="id", default=None)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "60c72b2f9b1d8e234c8f4b5a",
                "name": "Nguyễn Văn A",
                "code": "KH-0001",
                "phone": "0987654321",
                "classification": "Tiềm năng",
                "address": "123 Đường ABC, Quận 1, TP. HCM",
                "email": "nguyenvana@gmail.com",
                "source": "Website",
                "needs": "Tìm chung cư 2 phòng ngủ giá dưới 3 tỷ",
                "note": "Khách thiện chí, cần gọi lại vào cuối tuần",
                "createdAt": "2026-06-05T22:38:00+07:00"
            }
        }
    }


# 2. ADVISORY MODELS (TƯ VẤN)
class AdvisoryBase(BaseModel):
    name: str
    phone: str
    details: str
    productSlug: Optional[str] = None
    productName: Optional[str] = None
    status: str = "Mới"  # e.g. "Mới", "Đã liên hệ", "Đang xử lý", "Đóng"
    createdAt: Optional[str] = None

class AdvisoryCreate(AdvisoryBase):
    pass

class AdvisoryResponse(AdvisoryBase):
    id: Optional[PyObjectId] = Field(validation_alias="_id", serialization_alias="id", default=None)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "60c72b2f9b1d8e234c8f4b5b",
                "name": "Trần Thị B",
                "phone": "0912345678",
                "details": "Tôi muốn đăng ký xem thực tế căn hộ Vinhomes",
                "productSlug": "can-ho-panorama-masteri-west-heights-toa-a",
                "productName": "Căn Hộ Panorama Masteri West Heights - Tòa A View Trọn Hồ Trung Tâm",
                "status": "Mới",
                "createdAt": "2026-06-05T22:38:00+07:00"
            }
        }
    }


# 3. NEWSLETTER MODELS (ĐĂNG KÝ NHẬN TIN TỨC)
class NewsletterBase(BaseModel):
    email: EmailStr
    createdAt: Optional[str] = None
    active: bool = True

class NewsletterCreate(NewsletterBase):
    pass

class NewsletterResponse(NewsletterBase):
    id: Optional[PyObjectId] = Field(validation_alias="_id", serialization_alias="id", default=None)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "60c72b2f9b1d8e234c8f4b5c",
                "email": "subscriber@domain.com",
                "createdAt": "2026-06-05T22:38:00+07:00",
                "active": True
            }
        }
    }
