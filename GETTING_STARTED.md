# 🚀 Начало работы с проектом

Пошаговое руководство по запуску интернет-магазина ножей и топоров.

## 📋 Предварительные требования

Убедитесь, что у вас установлено:

- **Git** (2.0+)
- **Docker** (20.10+)
- **Docker Compose** (2.0+)
- **Node.js** (18+) - для frontend разработки
- **Python** (3.11+) - для backend разработки

## 🎯 Этап 1: Клонирование и настройка

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/yourusername/knife-store.git
cd knife-store
```

### 2. Скопируйте файл окружения

```bash
cp .env.example .env
```

### 3. Отредактируйте .env файл

Откройте `.env` и настройте следующие критически важные параметры:

```env
# PostgreSQL
POSTGRES_PASSWORD=ваш_надёжный_пароль

# MinIO
MINIO_ROOT_PASSWORD=ваш_надёжный_пароль

# Django
DJANGO_SECRET_KEY=сгенерируйте_свой_секретный_ключ

# ЮKassa (получить на https://yookassa.ru/)
YUKASSA_SHOP_ID=ваш_shop_id
YUKASSA_SECRET_KEY=ваш_secret_key

# Email
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Telegram Bot (получить у @BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token
```

## 🐳 Этап 2: Запуск через Docker Compose

### 1. Запустите все сервисы

```bash
docker-compose up -d
```

Это запустит:
- PostgreSQL (порт 5432)
- Redis (порт 6379)
- MinIO (порты 9000, 9001)
- Catalog Service (порт 8001)
- Order Service (порт 8002)
- Payment Service (порт 8003)
- Notification Service (порт 8004)
- Admin Panel (порт 8000)
- Frontend (порт 3000)
- Prometheus (порт 9090)
- Grafana (порт 3001)

### 2. Проверьте статус сервисов

```bash
docker-compose ps
```

Все сервисы должны быть в статусе "Up".

### 3. Примените миграции базы данных

```bash
# Catalog Service
docker-compose exec catalog-service alembic upgrade head

# Order Service
docker-compose exec order-service alembic upgrade head

# Admin Panel (Django)
docker-compose exec admin-panel python manage.py migrate
```

### 4. Создайте суперпользователя для админ-панели

```bash
docker-compose exec admin-panel python manage.py createsuperuser
```

Введите:
- Email: admin@knife-store.ru
- Password: (ваш пароль)

### 5. Загрузите тестовые данные (опционально)

```bash
docker-compose exec admin-panel python manage.py loaddata fixtures/initial_data.json
```

## 🌐 Этап 3: Проверка работоспособности

Откройте в браузере:

### Frontend
- **Главная страница**: http://localhost:3000

### Backend APIs
- **Catalog API**: http://localhost:8001/docs
- **Order API**: http://localhost:8002/docs
- **Payment API**: http://localhost:8003/docs
- **Notification API**: http://localhost:8004/docs

### Admin Panel
- **Django Admin**: http://localhost:8000/admin
  - Email: admin@knife-store.ru
  - Password: (ваш пароль)

### Инфраструктура
- **MinIO Console**: http://localhost:9001
  - Username: minioadmin
  - Password: (из .env)
  
- **Grafana**: http://localhost:3001
  - Username: admin
  - Password: (из .env)

- **Prometheus**: http://localhost:9090

## 🧪 Этап 4: Тестирование API

### Создать категорию (через Admin Panel или напрямую в БД)

```sql
-- Подключитесь к PostgreSQL
docker-compose exec postgres psql -U postgres -d knife_store

-- Вставьте тестовую категорию
INSERT INTO categories (id, name, slug, description, is_active)
VALUES (
  gen_random_uuid(),
  'Охотничьи ножи',
  'hunting-knives',
  'Профессиональные ножи для охоты',
  true
);
```

### Создать товар через API

```bash
curl -X POST "http://localhost:8001/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Охотничий нож Bear",
    "slug": "hunting-knife-bear",
    "description": "Надёжный нож для охоты",
    "price": 3500,
    "status": "in_stock",
    "blade_length": 15.0,
    "blade_material": "Сталь 95Х18",
    "handle_material": "Орех",
    "weight": 300,
    "hardness_hrc": "58-60",
    "purpose": "Охота, туризм",
    "stock_quantity": 25,
    "is_featured": true,
    "is_new": true
  }'
```

### Получить список товаров

```bash
curl "http://localhost:8001/api/v1/products?page=1&page_size=10"
```

## 💻 Этап 5: Локальная разработка (без Docker)

Если вы хотите разрабатывать локально:

### Backend (Catalog Service пример)

```bash
cd services/catalog

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt

# Запустите сервис
uvicorn app.main:app --reload --port 8001
```

### Frontend

```bash
cd frontend

# Установите зависимости
npm install

# Запустите dev-сервер
npm run dev
```

## 📊 Этап 6: Мониторинг

### Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f catalog-service
```

### Метрики в Grafana

1. Откройте http://localhost:3001
2. Войдите (admin/admin)
3. Откройте дашборды:
   - Services Overview
   - Database Metrics
   - API Performance

## 🛠️ Полезные команды

### Остановить все сервисы

```bash
docker-compose down
```

### Остановить и удалить все данные

```bash
docker-compose down -v
```

### Пересобрать сервисы

```bash
docker-compose up -d --build
```

### Выполнить команду внутри контейнера

```bash
docker-compose exec <service-name> <command>
```

### Посмотреть использование ресурсов

```bash
docker stats
```

## 🔧 Troubleshooting

### Проблема: Порт уже занят

Измените порт в `docker-compose.yml` или остановите конфликтующий сервис.

### Проблема: Ошибка подключения к БД

```bash
# Проверьте, что PostgreSQL запущен
docker-compose ps postgres

# Проверьте логи
docker-compose logs postgres
```

### Проблема: Миграции не применяются

```bash
# Сбросьте миграции
docker-compose exec catalog-service alembic downgrade base
docker-compose exec catalog-service alembic upgrade head
```

### Проблема: Frontend не загружается

```bash
# Пересоберите frontend
docker-compose up -d --build frontend

# Проверьте логи
docker-compose logs frontend
```

## 📚 Следующие шаги

1. ✅ **Ознакомьтесь с документацией API** - http://localhost:8001/docs
2. ✅ **Изучите структуру проекта** - см. README.md
3. ✅ **Настройте IDE** - рекомендуем VS Code с расширениями Python и ESLint
4. ✅ **Прочитайте гайд по контрибьютингу** - CONTRIBUTING.md
5. ✅ **Присоединяйтесь к команде** - создавайте issues и pull requests

## 🎉 Готово!

Ваш интернет-магазин ножей и топоров запущен и готов к разработке!

Если у вас возникли проблемы, создайте issue на GitHub или свяжитесь с командой.