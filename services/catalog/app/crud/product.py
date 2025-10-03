"""
CRUD операции для работы с товарами
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import selectinload
from typing import Optional, List
from uuid import UUID

from app.db.models import Product, ProductImage, Category
from app.schemas.product import ProductCreate, ProductUpdate, ProductFilter


class ProductCRUD:
    """CRUD операции для товаров"""

    @staticmethod
    async def get_by_id(db: AsyncSession, product_id: UUID) -> Optional[Product]:
        """Получить товар по ID"""
        query = select(Product).options(
            selectinload(Product.images),
            selectinload(Product.category)
        ).where(Product.id == product_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_slug(db: AsyncSession, slug: str) -> Optional[Product]:
        """Получить товар по slug"""
        query = select(Product).options(
            selectinload(Product.images),
            selectinload(Product.category)
        ).where(Product.slug == slug)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_list(
        db: AsyncSession,
        filters: ProductFilter
    ) -> tuple[List[Product], int]:
        """Получить список товаров с фильтрацией и пагинацией"""
        
        # Базовый запрос
        query = select(Product).options(
            selectinload(Product.images),
            selectinload(Product.category)
        )
        
        # Применение фильтров
        conditions = []
        
        if filters.category_id:
            conditions.append(Product.category_id == filters.category_id)
        
        if filters.min_price is not None:
            conditions.append(Product.price >= filters.min_price)
        
        if filters.max_price is not None:
            conditions.append(Product.price <= filters.max_price)
        
        if filters.status:
            conditions.append(Product.status == filters.status)
        
        if filters.blade_material:
            conditions.append(Product.blade_material.ilike(f"%{filters.blade_material}%"))
        
        if filters.min_blade_length is not None:
            conditions.append(Product.blade_length >= filters.min_blade_length)
        
        if filters.max_blade_length is not None:
            conditions.append(Product.blade_length <= filters.max_blade_length)
        
        if filters.min_weight is not None:
            conditions.append(Product.weight >= filters.min_weight)
        
        if filters.max_weight is not None:
            conditions.append(Product.weight <= filters.max_weight)
        
        if filters.hardness_hrc:
            conditions.append(Product.hardness_hrc == filters.hardness_hrc)
        
        if filters.purpose:
            conditions.append(Product.purpose.ilike(f"%{filters.purpose}%"))
        
        if filters.is_featured is not None:
            conditions.append(Product.is_featured == filters.is_featured)
        
        if filters.is_new is not None:
            conditions.append(Product.is_new == filters.is_new)
        
        if filters.search:
            search_term = f"%{filters.search}%"
            conditions.append(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                    Product.blade_material.ilike(search_term),
                    Product.purpose.ilike(search_term)
                )
            )
        
        if conditions:
            query = query.where(and_(*conditions))
        
        # Подсчёт общего количества
        count_query = select(func.count()).select_from(Product)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Сортировка
        sort_column = getattr(Product, filters.sort_by, Product.created_at)
        if filters.sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Пагинация
        offset = (filters.page - 1) * filters.page_size
        query = query.offset(offset).limit(filters.page_size)
        
        result = await db.execute(query)
        products = result.scalars().all()
        
        return products, total

    @staticmethod
    async def create(
        db: AsyncSession,
        product_data: ProductCreate
    ) -> Product:
        """Создать новый товар"""
        # Извлекаем изображения из данных
        images_data = product_data.images if hasattr(product_data, 'images') else []
        product_dict = product_data.model_dump(exclude={'images'})
        
        # Создаём товар
        product = Product(**product_dict)
        db.add(product)
        await db.flush()
        
        # Добавляем изображения
        for idx, image_data in enumerate(images_data):
            image = ProductImage(
                product_id=product.id,
                **image_data.model_dump()
            )
            db.add(image)
        
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def update(
        db: AsyncSession,
        product_id: UUID,
        product_data: ProductUpdate
    ) -> Optional[Product]:
        """Обновить товар"""
        product = await ProductCRUD.get_by_id(db, product_id)
        if not product:
            return None
        
        update_data = product_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def delete(db: AsyncSession, product_id: UUID) -> bool:
        """Удалить товар"""
        product = await ProductCRUD.get_by_id(db, product_id)
        if not product:
            return False
        
        await db.delete(product)
        await db.commit()
        return True

    @staticmethod
    async def increment_view_count(db: AsyncSession, product_id: UUID) -> None:
        """Увеличить счётчик просмотров"""
        product = await ProductCRUD.get_by_id(db, product_id)
        if product:
            product.view_count += 1
            await db.commit()

    @staticmethod
    async def get_featured(db: AsyncSession, limit: int = 10) -> List[Product]:
        """Получить избранные товары"""
        query = select(Product).options(
            selectinload(Product.images)
        ).where(Product.is_featured == True).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_new(db: AsyncSession, limit: int = 10) -> List[Product]:
        """Получить новинки"""
        query = select(Product).options(
            selectinload(Product.images)
        ).where(Product.is_new == True).order_by(Product.created_at.desc()).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()


class CategoryCRUD:
    """CRUD операции для категорий"""

    @staticmethod
    async def get_by_id(db: AsyncSession, category_id: UUID) -> Optional[Category]:
        """Получить категорию по ID"""
        query = select(Category).where(Category.id == category_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_slug(db: AsyncSession, slug: str) -> Optional[Category]:
        """Получить категорию по slug"""
        query = select(Category).where(Category.slug == slug)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession, is_active: Optional[bool] = None) -> List[Category]:
        """Получить все категории"""
        query = select(Category).order_by(Category.sort_order, Category.name)
        
        if is_active is not None:
            query = query.where(Category.is_active == is_active)
        
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_with_product_count(db: AsyncSession) -> List[tuple]:
        """Получить категории с количеством товаров"""
        query = select(
            Category,
            func.count(Product.id).label('product_count')
        ).outerjoin(Product).group_by(Category.id).order_by(Category.sort_order)
        
        result = await db.execute(query)
        return result.all()