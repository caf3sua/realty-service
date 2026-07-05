from fastapi import APIRouter, HTTPException, BackgroundTasks
import httpx
import os
import uuid
import asyncio
from pydantic import BaseModel
from typing import Optional, List
from app.core.config import settings

try:
    from zlapi import ZaloAPI
    from zlapi.models import Message, ThreadType
except ImportError:
    pass

router = APIRouter(
    prefix="/zalo",
    tags=["Zalo"]
)

class ZaloMessageRequest(BaseModel):
    thread_id: str  # ID của user hoặc ID của group
    is_group: bool = False  # True nếu gửi vào group
    text: Optional[str] = None
    image_urls: Optional[List[str]] = []

def _send_zalo_sync(thread_id: str, is_group: bool, text: Optional[str], image_paths: List[str]):
    """Đăng nhập và gửi tin nhắn qua zlapi bằng một thread riêng"""
    if not all([settings.ZALO_PHONE, settings.ZALO_PASSWORD, settings.ZALO_IMEI, settings.ZALO_COOKIE]):
        raise ValueError("Chưa cấu hình đầy đủ ZALO_PHONE, ZALO_PASSWORD, ZALO_IMEI, ZALO_COOKIE trong .env")

    # Khởi tạo ZaloAPI
    client = ZaloAPI(
        settings.ZALO_PHONE, 
        settings.ZALO_PASSWORD, 
        imei=settings.ZALO_IMEI, 
        cookie=settings.ZALO_COOKIE
    )
    
    # Lựa chọn loại Thread
    thread_type = ThreadType.GROUP if is_group else ThreadType.USER
    msg = Message(text=text) if text else None
    
    if image_paths:
        if len(image_paths) == 1:
            # Gửi 1 ảnh
            client.sendLocalImage(image_paths[0], thread_id=thread_id, thread_type=thread_type, message=msg)
        else:
            # Gửi nhiều ảnh
            client.sendMultiLocalImage(image_paths, thread_id=thread_id, thread_type=thread_type, message=msg)
    elif msg:
        # Gửi text đơn thuần
        client.send(msg, thread_id=thread_id, thread_type=thread_type)
    else:
        raise ValueError("Yêu cầu có ít nhất text hoặc image_urls")

def _get_zalo_client():
    if not all([settings.ZALO_PHONE, settings.ZALO_PASSWORD, settings.ZALO_IMEI, settings.ZALO_COOKIE]):
        raise ValueError("Chưa cấu hình đầy đủ ZALO_PHONE, ZALO_PASSWORD, ZALO_IMEI, ZALO_COOKIE trong .env")
    return ZaloAPI(
        settings.ZALO_PHONE, 
        settings.ZALO_PASSWORD, 
        imei=settings.ZALO_IMEI, 
        cookie=settings.ZALO_COOKIE
    )

@router.get("/friends")
async def get_zalo_friends():
    """Lấy danh sách bạn bè Zalo để lấy thread_id (user_id)"""
    try:
        def fetch_sync():
            client = _get_zalo_client()
            return client.fetchAllFriends()
            
        friends = await asyncio.to_thread(fetch_sync)
        return {"status": "success", "data": friends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lấy danh sách bạn bè: {str(e)}")

@router.get("/groups")
async def get_zalo_groups():
    """Lấy danh sách các nhóm Zalo (group) để lấy thread_id (group_id)"""
    try:
        def fetch_sync():
            client = _get_zalo_client()
            return client.fetchAllGroups()
            
        groups = await asyncio.to_thread(fetch_sync)
        return {"status": "success", "data": groups}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lấy danh sách nhóm: {str(e)}")

async def download_image(http_client, url, temp_dir):
    try:
        response = await http_client.get(url)
        response.raise_for_status()
        
        # Lưu file tạm với extension tùy ý (thường S3 sẽ trả về ảnh jpg/png)
        ext = url.split(".")[-1][:4] if "." in url else "jpg"
        image_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}.{ext}")
        with open(image_path, "wb") as f:
            f.write(response.content)
        return image_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Không thể tải ảnh từ {url}: {str(e)}")

@router.post("/send-message")
async def send_zalo_message(request: ZaloMessageRequest):
    """
    Gửi tin nhắn hoặc nhiều hình ảnh qua Zalo cá nhân (cá nhân hoặc group) sử dụng thư viện zlapi.
    """
    if not request.text and not request.image_urls:
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp text hoặc image_urls")

    image_paths = []
    
    # Nếu có image_urls, tải đồng loạt các ảnh xuống tạm thời
    if request.image_urls:
        temp_dir = os.path.join(os.path.dirname(__file__), "..", "..", "tmp")
        os.makedirs(temp_dir, exist_ok=True)
        
        async with httpx.AsyncClient() as http_client:
            tasks = [download_image(http_client, url, temp_dir) for url in request.image_urls]
            image_paths = await asyncio.gather(*tasks)

    # Gửi tin nhắn qua Zalo (chạy trong thread để không block event loop của FastAPI)
    try:
        await asyncio.to_thread(_send_zalo_sync, request.thread_id, request.is_group, request.text, image_paths)
    except Exception as e:
        # Dọn dẹp file tạm nếu có lỗi
        for path in image_paths:
            if os.path.exists(path):
                os.remove(path)
        raise HTTPException(status_code=500, detail=f"Lỗi khi gửi qua Zalo: {str(e)}")
        
    # Gửi thành công, dọn dẹp file tạm
    for path in image_paths:
        if os.path.exists(path):
            os.remove(path)

    return {"status": "success", "message": "Gửi tin nhắn qua Zalo cá nhân thành công"}
