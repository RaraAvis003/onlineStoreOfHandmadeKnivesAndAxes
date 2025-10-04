"""
Микросервис каталога товаров
Управление товарами, категориями, фильтрация и поиск
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.api.v1 import api_router

app = FastAPI(
    title="Knife Store - Catalog Service",
    description="API для управления каталогом товаров (ножи и топоры)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware для сжатия ответов
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Prometheus метрики
Instrumentator().instrument(app).expose(app)

# Подключение роутеров
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "service": "Catalog Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {
        "status": "healthy",
        "service": "catalog-service"
    }


@app.on_event("startup")
async def startup_event():
    """Действия при запуске приложения"""
    print("🚀 Catalog Service starting...")


@app.on_event("shutdown")
async def shutdown_event():
    """Действия при остановке приложения"""
    print("👋 Catalog Service shutting down...")