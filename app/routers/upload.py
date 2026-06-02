from fastapi import APIRouter, UploadFile, File, HTTPException, status
import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
import uuid
import os

router = APIRouter(prefix="/api/upload", tags=["Upload"])

@router.post("")
async def upload_file(file: UploadFile = File(...)):
    # Extract file extension and generate unique filename
    _, ext = os.path.splitext(file.filename or "")
    if not ext:
        # Fallback to check content type if extension not in filename
        if file.content_type == "image/png":
            ext = ".png"
        elif file.content_type == "image/jpeg":
            ext = ".jpg"
        elif file.content_type == "image/gif":
            ext = ".gif"
        elif file.content_type == "image/svg+xml":
            ext = ".svg"
        else:
            ext = ".bin"

    unique_filename = f"{uuid.uuid4().hex}{ext}"
    s3_key = f"logos/{unique_filename}"
    
    try:
        # Initialize boto3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_ACCESS_SECRET,
            endpoint_url=settings.S3_ENDPOINT,
            region_name=settings.S3_REGION,
            verify=settings.S3_VERIFY,
        )
        
        contents = await file.read()
        content_type = file.content_type or "application/octet-stream"
        
        # Try uploading with public-read ACL first
        try:
            s3_client.put_object(
                Bucket=settings.S3_BUCKET,
                Key=s3_key,
                Body=contents,
                ContentType=content_type,
                ACL="public-read"
            )
        except ClientError as acl_err:
            # Fallback if ACL is not supported/allowed on the bucket
            err_msg = str(acl_err)
            if any(term in err_msg for term in ["AccessDenied", "InvalidBucketAcl", "NotImplemented", "MethodNotAllowed"]):
                s3_client.put_object(
                    Bucket=settings.S3_BUCKET,
                    Key=s3_key,
                    Body=contents,
                    ContentType=content_type
                )
            else:
                raise acl_err
        
        # Construct URL
        endpoint = settings.S3_ENDPOINT.rstrip("/")
        file_url = f"{endpoint}/{settings.S3_BUCKET}/{s3_key}"
        
        return {"url": file_url}
        
    except ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"S3 client error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )
