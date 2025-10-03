"""
API endpoints для работы с товарами
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
import math

from app.db.database import get_db
from app.schemas.product import (
    ProductResponse,
    ProductCreate,
    ProductUpdate,
    ProductListResponse,
    ProductFilter
)
from app.crud.product import ProductCRUD

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=ProductListResponse)
async def get_products(
    category_id: Optional[UUID] = Query(None, description="Фильтр по категории"),
    min_price: Optional[float] = Query(None, ge=0, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, ge=0, description="Максимальная цена"),
    status: Optional[str] = Query(None, description="Статус товара"),
    blade_material: Optional[str] = Query(None, description="Материал клинка"),
    min_blade_length: Optional[float] = Query(None, ge=0, description="Минимальная длина клинка"),
    max_blade_length: Optional[float] = Query(None, ge=0, description="Максимальная длина клинка"),
    min_weight: Optional[float] = Query(None, ge=0, description="Минимальный вес"),
    max_weight: Optional[float] = Query(None, ge=0, description="Максимальный вес"),
    hardness_hrc: Optional[str] = Query(None, description="Твёрдость HRC"),
    purpose: Optional[str] = Query(None, description="Назначение"),
    is_featured: Optional[bool] = Query(None, description="Избранные"),
    is_new: Optional[bool] = Query(None, description="Новинки"),
    search: Optional[str] = Query(None, description="Поиск по названию и описанию"),
    sort_by: str = Query("created_at", pattern="^(price|created_at|rating|view_count)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список товаров с фильтрацией и пагинацией
    
    Параметры фильтрации:
    - **category_id**: UUID категории
    - **min_price/max_price**: Диапазон цен
    - **status**: Статус товара (in_stock, on_order, discontinued)
    - **blade_material**: Материал клинка
    - **min_blade_length/max_blade_length**: Диапазон длины клинка (см)
    - **min_weight/max_weight**: Диапазон веса (г)
    - **hardness_hrc**: Твёрдость по шкале HRC
    - **purpose**: Назначение товара
    - **is_featured**: Только избранные товары
    - **is_new**: Только новинки
    - **search**: Поиск по названию, описанию, материалу
    
    Сортировка:
    - **sort_by**: Поле для сортировки (price, created_at, rating, view_count)
    - **sort_order**: Направление (asc, desc)
    """
    filters = ProductFilter(
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        status=status,
        blade_material=blade_material,
        min_blade_length=min_blade_length,
        max_blade_length=max_blade_length,
        min_weight=min_weight,
        max_weight=max_weight,
        hardness_hrc=hardness_hrc,
        purpose=purpose,
        is_featured=is_featured,
        is_new=is_new,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )
    
    products, total = await ProductCRUD.get_list(db, filters)
    total_pages = math.ceil(total / page_size)
    
    return ProductListResponse(
        items=products,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/featured", response_model=list[ProductResponse])
async def get_featured_products(
    limit: int = Query(10, ge=1, le=50, description="Количество товаров"),
    db: AsyncSession = Depends(get_db)
):
    """Получить избранные товары"""
    products = await ProductCRUD.get_featured(db, limit)
    return products


@router.get("/new", response_model=list[ProductResponse])
async def get_new_products(
    limit: int = Query(10, ge=1, le=50, description="Количество товаров"),
    db: AsyncSession = Depends(get_db)
):
    """Получить новинки"""
    products = await ProductCRUD.get_new(db, limit)
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Получить товар по ID"""
    product = await ProductCRUD.get_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    
    # Увеличиваем счётчик просмотров
    await ProductCRUD.increment_view_count(db, product_id)
    
    return product


@router.get("/slug/{slug}", response_model=ProductResponse)
async def get_product_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Получить товар по slug"""
    product = await ProductCRUD.get_by_slug(db, slug)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    
    # Увеличиваем счётчик просмотров
    await ProductCRUD.increment_view_count(db, product.id)
    
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Создать новый товар
    
    Требуется аутентификация с правами администратора
    """
    # TODO: Добавить проверку прав доступа
    
    # Проверка уникальности slug
    existing = await ProductCRUD.get_by_slug(db, product_data.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Товар с таким slug уже существует"
        )
    
    product = await ProductCRUD.create(db, product_data)
    return product


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить товар
    
    Требуется аутентификация с правами администратора
    """
    # TODO: Добавить проверку прав доступа
    
    # Проверка уникальности slug при обновлении
    if product_data.slug:
        existing = await ProductCRUD.get_by_slug(db, product_data.slug)
        if existing and existing.id != product_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Товар с таким slug уже существует"
            )
    
    product = await ProductCRUD.update(db, product_id, product_data)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Удалить товар
    
    Требуется аутентификация с правами администратора
    """
    # TODO: Добавить проверку прав доступа
    
    success = await ProductCRUD.delete(db, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    
    return None