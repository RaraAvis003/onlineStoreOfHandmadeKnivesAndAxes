"""
Модели базы данных для каталога товаров
"""
from sqlalchemy import Column, String, Text, Numeric, Integer, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.db.database import Base


class ProductStatus(str, enum.Enum):
    """Статусы товара"""
    IN_STOCK = "in_stock"
    ON_ORDER = "on_order"
    DISCONTINUED = "discontinued"


class Category(Base):
    """Модель категории товаров"""
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"))
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    products = relationship("Product", back_populates="category")
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")

    def __repr__(self):
        return f"<Category(name='{self.name}', slug='{self.slug}')>"


class Product(Base):
    """Модель товара"""
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"))
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    old_price = Column(Numeric(10, 2))
    status = Column(
        ENUM(ProductStatus, name="product_status", create_type=False),
        default=ProductStatus.IN_STOCK
    )

    # Характеристики
    blade_length = Column(Numeric(5, 2))  # см
    blade_material = Column(String(100))
    handle_material = Column(String(100))
    weight = Column(Numeric(6, 2))  # граммы
    hardness_hrc = Column(String(10))
    purpose = Column(String(255))

    # Дополнительные поля
    stock_quantity = Column(Integer, default=0)
    min_order_quantity = Column(Integer, default=1)
    max_order_quantity = Column(Integer)
    is_featured = Column(Boolean, default=False, index=True)
    is_new = Column(Boolean, default=False, index=True)
    view_count = Column(Integer, default=0)
    rating = Column(Numeric(3, 2), default=0)
    review_count = Column(Integer, default=0)

    # SEO
    meta_title = Column(String(255))
    meta_description = Column(Text)
    meta_keywords = Column(String(500))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"


class ProductImage(Base):
    """Модель изображения товара"""
    __tablename__ = "product_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    is_main = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    product = relationship("Product", back_populates="images")

    def __repr__(self):
        return f"<ProductImage(product_id='{self.product_id}', is_main={self.is_main})>"