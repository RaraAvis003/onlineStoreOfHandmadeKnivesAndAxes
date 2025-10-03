# Catalog Service - Микросервис каталога товаров

Микросервис для управления каталогом товаров (ножей и топоров) с поддержкой фильтрации, поиска и пагинации.

## Возможности

- ✅ CRUD операции для товаров и категорий
- ✅ Расширенная фильтрация (цена, материал, размеры, и т.д.)
- ✅ Полнотекстовый поиск
- ✅ Пагинация результатов
- ✅ Счётчик просмотров
- ✅ Поддержка изображений товаров
- ✅ RESTful API с документацией (Swagger/ReDoc)
- ✅ Метрики Prometheus

## Технологии

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM
- **PostgreSQL** - база данных
- **Alembic** - миграции БД
- **Redis** - кэширование
- **Pydantic** - валидация данных

## Структура проекта

```
catalog/
├── alembic/              # Миграции БД
│   ├── versions/
│   └── env.py
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── products.py    # Endpoints для товаров
│   │       ├── categories.py  # Endpoints для категорий
│   │       └── __init__.py
│   ├── core/
│   │   └── config.py          # Конфигурация
│   ├── crud/
│   │   └── product.py         # CRUD операции
│   ├── db/
│   │   ├── database.py        # Настройки БД
│   │   └── models.py          # SQLAlchemy модели
│   ├── schemas/
│   │   └── product.py         # Pydantic схемы
│   └── main.py                # Точка входа
├── tests/                     # Тесты
├── Dockerfile
├── requirements.txt
└── alembic.ini
```

## Локальная разработка

### 1. Установка зависимостей

```bash
cd services/catalog
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Создайте файл `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/knife_store
REDIS_URL=redis://localhost:6379/0
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

### 3. Применение миграций

```bash
alembic upgrade head
```

### 4. Создание новой миграции (при изменении моделей)

```bash
alembic revision --autogenerate -m "Описание изменений"
alembic upgrade head
```

### 5. Запуск сервиса

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Сервис будет доступен по адресу: http://localhost:8000

## API Документация

После запуска сервиса документация доступна по следующим URL:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Основные endpoints

### Товары

```
GET    /api/v1/products          - Список товаров с фильтрацией
GET    /api/v1/products/{id}     - Получить товар по ID
GET    /api/v1/products/slug/{slug} - Получить товар по slug
GET    /api/v1/products/featured - Избранные товары
GET    /api/v1/products/new      - Новинки
POST   /api/v1/products          - Создать товар
PATCH  /api/v1/products/{id}     - Обновить товар
DELETE /api/v1/products/{id}     - Удалить товар
```

### Категории

```
GET    /api/v1/categories           - Список категорий
GET    /api/v1/categories/with-count - Категории с кол-вом товаров
GET    /api/v1/categories/{id}      - Получить категорию по ID
GET    /api/v1/categories/slug/{slug} - Получить категорию по slug
```

## Примеры использования

### Получить список товаров с фильтрацией

```bash
curl "http://localhost:8000/api/v1/products?min_price=1000&max_price=5000&blade_material=сталь&sort_by=price&sort_order=asc&page=1&page_size=20"
```

### Поиск товаров

```bash
curl "http://localhost:8000/api/v1/products?search=охотничий нож"
```

### Создать новый товар

```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Охотничий нож",
    "slug": "hunting-knife",
    "description": "Качественный охотничий нож",
    "price": 2500,
    "status": "in_stock",
    "blade_length": 12.5,
    "blade_material": "Сталь 95Х18",
    "handle_material": "Орех",
    "weight": 250,
    "hardness_hrc": "58-60",
    "purpose": "Охота",
    "stock_quantity": 10
  }'
```

## Запуск через Docker

```bash
# Из корня проекта
docker-compose up catalog-service
```

## Тестирование

```bash
pytest tests/ -v --cov=app
```

## Мониторинг

Метрики Prometheus доступны по адресу: http://localhost:8000/metrics

## Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| DATABASE_URL | URL базы данных PostgreSQL | - |
| REDIS_URL | URL Redis | redis://localhost:6379/0 |
| REDIS_CACHE_TTL | Время жизни кэша (сек) | 3600 |
| MINIO_ENDPOINT | Endpoint MinIO | localhost:9000 |
| MINIO_ACCESS_KEY | MinIO Access Key | - |
| MINIO_SECRET_KEY | MinIO Secret Key | - |
| MINIO_BUCKET_NAME | Имя bucket для изображений | products |
| DEFAULT_PAGE_SIZE | Размер страницы по умолчанию | 20 |
| MAX_PAGE_SIZE | Максимальный размер страницы | 100 |
| LOG_LEVEL | Уровень логирования | INFO |

## Troubleshooting

### Ошибка подключения к БД

Убедитесь, что PostgreSQL запущен и доступен:
```bash
psql -h localhost -U postgres -d knife_store
```

### Ошибка миграций

Сбросить все миграции и применить заново:
```bash
alembic downgrade base
alembic upgrade head
```

## Дальнейшая разработка

- [ ] Добавить JWT аутентификацию
- [ ] Реализовать кэширование через Redis
- [ ] Добавить загрузку изображений в MinIO
- [ ] Настроить rate limiting
- [ ] Добавить webhook уведомления при изменении товаров