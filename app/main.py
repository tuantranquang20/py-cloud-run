import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, items

# Lấy metadata từ environment variable (được inject bởi CI/CD)
APP_VERSION = os.environ.get("APP_VERSION", "0.0.1")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

app = FastAPI(
    title="My App",
    description="Demo app để test CI/CD workflow: GitHub Actions → GCS → Cloud Function → Cloud Build → Cloud Run",
    version=APP_VERSION,
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc UI
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký routers
app.include_router(health.router)
app.include_router(items.router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Hello from Cloud Run!",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "docs": "/docs",
    }
