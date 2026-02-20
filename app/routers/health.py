import os
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
async def health_check():
    """
    Health check endpoint — Cloud Run dùng endpoint này để kiểm tra container.
    Trả về 200 OK là đủ để LB/Cloud Run xác nhận app đang hoạt động.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": os.environ.get("APP_VERSION", "unknown"),
        "environment": os.environ.get("ENVIRONMENT", "development"),
    }

@router.get("/ready")
async def readiness_check():
    """
    Readiness check — kiểm tra app đã sẵn sàng nhận traffic chưa.
    Có thể mở rộng để kiểm tra kết nối DB, cache...
    """
    checks = {
        "app": "ok",
        # Ví dụ kiểm tra DB: "database": check_db_connection()
    }
    all_ok = all(v == "ok" for v in checks.values())
    return {
        "ready": all_ok,
        "checks": checks,
    }
