"""
Pydantic схемы для валидации данных товаров
"""
from pydantic import BaseModel, Field, UUID4, HttpUrl
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from app.db.models import ProductStatus


# Схемы для изображений
class ProductImageBase(BaseModel):
    """Базовая схема изображения"""
    image_url: str
    alt_text: Optional[str] = None
    is_main: bool = False
    sort_order: int = 0


class ProductImageCreate(ProductImageBase):
    """Схема создания изображения"""
    pass


class ProductImageResponse(ProductImageBase):
    """Схема ответа изображения"""
    id: UUID4
    product_id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True


# Схемы для категорий
class CategoryBase(BaseModel):
    """Базовая схема категории"""
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    """Схема создания категории"""
    parent_id: Optional[UUID4] = None


class CategoryUpdate(BaseModel):
    """Схема обновления категории"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    parent_id: Optional[UUID4] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class CategoryResponse(CategoryBase):
    """Схема ответа категории"""
    id: UUID4
    parent_id: Optional[UUID4] = None
    created_at: datetime
    updated_at: datetime
    product_count: Optional[int] = 0

    class Config:
        from_attributes = True


# Схемы для товаров
class ProductBase(BaseModel):
    """Базовая схема товара"""
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0, decimal_places=2)
    old_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    status: ProductStatus = ProductStatus.IN_STOCK
    
    # Характеристики
    blade_length: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    blade_material: Optional[str] = Field(None, max_length=100)
    handle_material: Optional[str] = Field(None, max_length=100)
    weight: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    hardness_hrc: Optional[str] = Field(None, max_length=10)
    purpose: Optional[str] = Field(None, max_length=255)
    
    # Дополнительные поля
    stock_quantity: int = Field(default=0, ge=0)
    min_order_quantity: int = Field(default=1, ge=1)
    max_order_quantity: Optional[int] = Field(None, gt=0)
    is_featured: bool = False
    is_new: bool = False
    
    # SEO
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = Field(None, max_length=500)


class ProductCreate(ProductBase):
    """Схема создания товара"""
    category_id: Optional[UUID4] = None
    images: Optional[List[ProductImageCreate]] = []


class ProductUpdate(BaseModel):
    """Схема обновления товара"""
    category_id: Optional[UUID4] = None
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    old_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    status: Optional[ProductStatus] = None
    
    blade_length: Optional[Decimal] = None
    blade_material: Optional[str] = None
    handle_material: Optional[str] = None
    weight: Optional[Decimal] = None
    hardness_hrc: Optional[str] = None
    purpose: Optional[str] = None
    
    stock_quantity: Optional[int] = Field(None, ge=0)
    min_order_quantity: Optional[int] = Field(None, ge=1)
    max_order_quantity: Optional[int] = None
    is_featured: Optional[bool] = None
    is_new: Optional[bool] = None
    
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None


class ProductResponse(ProductBase):
    """Схема ответа товара"""
    id: UUID4
    category_id: Optional[UUID4] = None
    view_count: int
    rating: Decimal
    review_count: int
    created_at: datetime
    updated_at: datetime
    images: List[ProductImageResponse] = []
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Схема списка товаров с пагинацией"""
    items: List[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# Схемы для фильтрации
class ProductFilter(BaseModel):
    """Схема фильтров для товаров"""
    category_id: Optional[UUID4] = None
    min_price: Optional[Decimal] = Field(None, ge=0)
    max_price: Optional[Decimal] = Field(None, ge=0)
    status: Optional[ProductStatus] = None
    blade_material: Optional[str] = None
    min_blade_length: Optional[Decimal] = None
    max_blade_length: Optional[Decimal] = None
    min_weight: Optional[Decimal] = None
    max_weight: Optional[Decimal] = None
    hardness_hrc: Optional[str] = None
    purpose: Optional[str] = None
    is_featured: Optional[bool] = None
    is_new: Optional[bool] = None
    search: Optional[str] = None
    sort_by: Optional[str] = Field(default="created_at", pattern="^(price|created_at|rating|view_count)$")
    sort_order: Optional[str] = Field(default="desc", pattern="^(asc|desc)$")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)