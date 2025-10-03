"""
API endpoints для работы с категориями
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.db.database import get_db
from app.schemas.product import CategoryResponse
from app.crud.product import CategoryCRUD

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryResponse])
async def get_categories(
    is_active: Optional[bool] = Query(None, description="Фильтр по активности"),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список всех категорий
    
    - **is_active**: Фильтровать только активные категории
    """
    categories = await CategoryCRUD.get_all(db, is_active)
    return categories


@router.get("/with-count", response_model=list[dict])
async def get_categories_with_product_count(
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список категорий с количеством товаров в каждой
    """
    result = await CategoryCRUD.get_with_product_count(db)
    
    # Форматируем результат
    categories_with_count = []
    for category, product_count in result:
        category_dict = {
            "id": category.id,
            "name": category.name,
            "slug": category.slug,
            "description": category.description,
            "parent_id": category.parent_id,
            "image_url": category.image_url,
            "is_active": category.is_active,
            "sort_order": category.sort_order,
            "product_count": product_count,
            "created_at": category.created_at,
            "updated_at": category.updated_at
        }
        categories_with_count.append(category_dict)
    
    return categories_with_count


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Получить категорию по ID"""
    category = await CategoryCRUD.get_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    return category


@router.get("/slug/{slug}", response_model=CategoryResponse)
async def get_category_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Получить категорию по slug"""
    category = await CategoryCRUD.get_by_slug(db, slug)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    return category