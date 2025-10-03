# Интернет-магазин ножей и топоров

## Архитектура проекта

Микросервисная архитектура на базе Kubernetes с следующими компонентами:

### Микросервисы
- **catalog-service** (FastAPI) - Каталог товаров, фильтрация, поиск
- **order-service** (FastAPI) - Корзина, заказы
- **payment-service** (FastAPI) - Интеграция с ЮKassa
- **notification-service** (FastAPI) - Email и Telegram уведомления
- **admin-panel** (Django) - Административная панель
- **frontend** (Next.js) - Клиентское приложение

### Инфраструктура
- **PostgreSQL** - Основная БД
- **Redis** - Кэширование и очереди
- **MinIO** - Хранилище изображений
- **Celery** - Асинхронные задачи

## Структура директорий

```
knife-store/
├── services/
│   ├── catalog/              # Микросервис каталога
│   │   ├── app/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── orders/               # Микросервис заказов
│   │   ├── app/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── payments/             # Микросервис платежей
│   │   ├── app/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── notifications/        # Микросервис уведомлений
│   │   ├── app/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   └── admin/                # Django админ-панель
│       ├── admin_panel/
│       ├── Dockerfile
│       ├── requirements.txt
│       └── tests/
├── frontend/                 # Next.js приложение
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   └── styles/
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   └── next.config.js
├── infrastructure/
│   ├── kubernetes/           # K8s манифесты
│   │   ├── catalog/
│   │   ├── orders/
│   │   ├── payments/
│   │   ├── notifications/
│   │   ├── admin/
│   │   ├── frontend/
│   │   └── base/
│   ├── terraform/            # Инфраструктура как код
│   └── monitoring/           # Prometheus, Grafana конфиги
├── shared/                   # Общий код
│   ├── proto/                # gRPC протоколы (опционально)
│   └── utils/
├── docker-compose.yml        # Для локальной разработки
├── docker-compose.prod.yml   # Для продакшена
├── .gitignore
├── .env.example
└── README.md
```

## Технологический стек

### Backend
- **Python 3.11+**
- **FastAPI** - Микросервисы
- **Django 5.0+** - Админ-панель
- **PostgreSQL 15+**
- **Redis 7+**
- **Celery** - Асинхронные задачи
- **SQLAlchemy** - ORM для FastAPI
- **Pydantic** - Валидация данных
- **Alembic** - Миграции БД

### Frontend
- **Next.js 14+** (App Router)
- **React 18+**
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui** - UI компоненты
- **React Query** - Управление состоянием
- **Zustand** - Глобальное состояние

### DevOps
- **Docker** & **Docker Compose**
- **Kubernetes**
- **Nginx Ingress Controller**
- **Prometheus** & **Grafana**
- **GitHub Actions** - CI/CD

## Быстрый старт (локальная разработка)

### Требования
- Docker 20.10+
- Docker Compose 2.0+
- Node.js 18+ (для frontend разработки)
- Python 3.11+ (для backend разработки)

### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/knife-store.git
cd knife-store
```

2. Скопируйте файл окружения:
```bash
cp .env.example .env
```

3. Запустите все сервисы:
```bash
docker-compose up -d
```

4. Применить миграции:
```bash
docker-compose exec catalog-service alembic upgrade head
docker-compose exec order-service alembic upgrade head
docker-compose exec admin-panel python manage.py migrate
```

5. Создайте суперпользователя для админ-панели:
```bash
docker-compose exec admin-panel python manage.py createsuperuser
```

### Доступ к сервисам

- **Frontend**: http://localhost:3000
- **Admin Panel**: http://localhost:8000/admin
- **Catalog API**: http://localhost:8001/docs
- **Order API**: http://localhost:8002/docs
- **Payment API**: http://localhost:8003/docs
- **Notification API**: http://localhost:8004/docs
- **MinIO Console**: http://localhost:9001
- **Grafana**: http://localhost:3001

## Этапы разработки

### ✅ Этап 1: Инфраструктура (Текущий)
- [x] Структура проекта
- [ ] Docker Compose конфигурация
- [ ] Базовые Dockerfile для всех сервисов
- [ ] .env файлы и конфигурация

### 🔄 Этап 2: Backend - Каталог товаров
- [ ] FastAPI приложение
- [ ] Модели данных (SQLAlchemy)
- [ ] CRUD операции
- [ ] Фильтрация и поиск
- [ ] API эндпоинты
- [ ] Тесты

### 📋 Этап 3: Backend - Заказы
- [ ] Модели корзины и заказов
- [ ] API для управления корзиной
- [ ] Оформление заказа
- [ ] Статусы заказов
- [ ] Тесты

### 💳 Этап 4: Backend - Платежи
- [ ] Интеграция с ЮKassa
- [ ] Webhook обработка
- [ ] Логирование транзакций
- [ ] Тесты

### 🔔 Этап 5: Backend - Уведомления
- [ ] Email отправка
- [ ] Telegram бот
- [ ] Celery задачи
- [ ] Шаблоны уведомлений
- [ ] Тесты

### 🛠️ Этап 6: Admin Panel
- [ ] Django настройка
- [ ] Модели админки
- [ ] Кастомные админ-формы
- [ ] Управление товарами
- [ ] Управление заказами

### 🎨 Этап 7: Frontend - Главная
- [ ] Next.js проект
- [ ] Hero-слайдер
- [ ] Секция "Новинки"
- [ ] Секция "Популярные категории"
- [ ] Адаптивный дизайн

### 📦 Этап 8: Frontend - Каталог
- [ ] Страница каталога
- [ ] Фильтры
- [ ] Сортировка
- [ ] Карточки товаров
- [ ] Пагинация

### 🔍 Этап 9: Frontend - Карточка товара
- [ ] Галерея изображений
- [ ] Характеристики
- [ ] Отзывы
- [ ] Кнопки действий

### 🛒 Этап 10: Frontend - Корзина и оформление
- [ ] Корзина
- [ ] Оформление заказа
- [ ] Форма доставки
- [ ] Выбор оплаты

### 👤 Этап 11: Личный кабинет
- [ ] Авторизация/Регистрация
- [ ] Профиль пользователя
- [ ] История заказов
- [ ] Избранное

### ☸️ Этап 12: Kubernetes
- [ ] Манифесты для всех сервисов
- [ ] Ingress конфигурация
- [ ] ConfigMaps и Secrets
- [ ] Persistent Volumes

### 📊 Этап 13: Мониторинг
- [ ] Prometheus настройка
- [ ] Grafana дашборды
- [ ] Алерты
- [ ] Логирование (ELK/Loki)

### 🚀 Этап 14: CI/CD
- [ ] GitHub Actions workflows
- [ ] Автоматические тесты
- [ ] Сборка Docker образов
- [ ] Деплой в Kubernetes

## Контрибьюторы

- Ваше имя - Backend Lead
- Команда разработки

## Лицензия

MIT