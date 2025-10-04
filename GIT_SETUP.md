# 🔄 Инициализация Git и push в GitHub

Пошаговая инструкция для создания репозитория и первого коммита.

## 📝 Шаг 1: Создайте репозиторий на GitHub

1. Перейдите на https://github.com
2. Нажмите кнопку **"New repository"**
3. Заполните поля:
   - **Repository name**: `knife-store`
   - **Description**: "Интернет-магазин ножей и топоров на микросервисной архитектуре"
   - **Visibility**: Public или Private
   - ⚠️ **НЕ** устанавливайте флаги "Add README" и "Add .gitignore"
4. Нажмите **"Create repository"**

## 🚀 Шаг 2: Инициализируйте локальный репозиторий

```bash
# Перейдите в корневую директорию проекта
cd knife-store

# Инициализируйте Git
git init

# Добавьте remote репозиторий (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/knife-store.git

# Проверьте, что remote добавлен
git remote -v
```

## 📦 Шаг 3: Создайте первый коммит

```bash
# Добавьте все файлы
git add .

# Создайте коммит
git commit -m "🎉 Initial commit: Project structure and Catalog Service

- Added project documentation (README, GETTING_STARTED)
- Implemented Catalog Service (FastAPI)
  - Product and Category models
  - CRUD operations
  - Advanced filtering and search
  - REST API with Swagger docs
- Docker Compose configuration for all services
- PostgreSQL database schema
- Alembic migrations setup
- Basic monitoring (Prometheus, Grafana)
- Stub services for Orders, Payments, Notifications
- Next.js frontend skeleton
"

# Переименуйте ветку в main (если нужно)
git branch -M main

# Отправьте код на GitHub
git push -u origin main
```

## 🏷️ Шаг 4: Создайте релиз (опционально)

```bash
# Создайте тег для первой версии
git tag -a v0.1.0 -m "Release v0.1.0: Catalog Service MVP"

# Отправьте тег на GitHub
git push origin v0.1.0
```

## 📋 Структура коммитов для следующих этапов

### Этап 2: Order Service

```bash
git checkout -b feature/order-service

# ... сделайте изменения ...

git add services/orders/
git commit -m "✨ feat: Implement Order Service

- Shopping cart functionality
- Order management
- Order status tracking
- Integration with Catalog Service
"

git push origin feature/order-service
# Создайте Pull Request на GitHub
```

### Этап 3: Payment Service

```bash
git checkout -b feature/payment-service

git add services/payments/
git commit -m "💳 feat: Implement Payment Service

- ЮKassa integration
- Webhook handling
- Payment status tracking
- Transaction logging
"

git push origin feature/payment-service
```

### Этап 4: Notification Service

```bash
git checkout -b feature/notification-service

git add services/notifications/
git commit -m "📧 feat: Implement Notification Service

- Email notifications (SMTP)
- Telegram bot integration
- Celery background tasks
- Notification templates
"

git push origin feature/notification-service
```

### Этап 5: Admin Panel

```bash
git checkout -b feature/admin-panel

git add services/admin/
git commit -m "🛠️ feat: Implement Django Admin Panel

- Product management
- Order management
- User management
- Custom admin forms
"

git push origin feature/admin-panel
```

### Этап 6: Frontend

```bash
git checkout -b feature/frontend

git add frontend/
git commit -m "🎨 feat: Implement Next.js Frontend

- Home page with Hero slider
- Product catalog with filters
- Product detail page
- Shopping cart
- Responsive design (Mobile-first)
"

git push origin feature/frontend
```

## 🔐 Важно: Безопасность

### Убедитесь, что .env файлы не попали в Git

```bash
# Проверьте статус
git status

# Если .env случайно добавлен, удалите его из индекса
git rm --cached .env
git commit -m "🔒 Remove .env from tracking"
```

### Добавьте GitHub Secrets для CI/CD

В настройках репозитория (Settings > Secrets and variables > Actions) добавьте:

- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- `POSTGRES_PASSWORD`
- `YUKASSA_SHOP_ID`
- `YUKASSA_SECRET_KEY`
- `SMTP_PASSWORD`
- `TELEGRAM_BOT_TOKEN`

## 📊 Настройка GitHub Projects

1. Перейдите в **Projects** на GitHub
2. Создайте новый проект "Knife Store Development"
3. Добавьте колонки:
   - 📋 Backlog
   - 🏗️ In Progress
   - 👀 Review
   - ✅ Done
4. Создайте issues для каждого этапа

## 🤝 Workflow для разработки

### Создание новой фичи

```bash
# Создайте ветку от main
git checkout main
git pull origin main
git checkout -b feature/your-feature-name

# Разработка...

# Коммиты
git add .
git commit -m "✨ feat: Description"

# Push и создание PR
git push origin feature/your-feature-name
# Создайте Pull Request на GitHub
```

### Именование коммитов (Conventional Commits)

Используйте следующие префиксы:

- `✨ feat:` - новая функциональность
- `🐛 fix:` - исправление бага
- `📝 docs:` - документация
- `💄 style:` - форматирование кода
- `♻️ refactor:` - рефакторинг
- `⚡ perf:` - оптимизация производительности
- `✅ test:` - тесты
- `🔧 chore:` - конфигурация, зависимости
- `🚀 deploy:` - деплой
- `🔒 security:` - безопасность

Примеры:

```bash
git commit -m "✨ feat(catalog): Add image upload to MinIO"
git commit -m "🐛 fix(orders): Fix cart total calculation"
git commit -m "📝 docs: Update API documentation"
git commit -m "♻️ refactor(payments): Simplify webhook handler"
```

## 🌳 Git Flow

```
main (production)
  ↓
develop (staging)
  ↓
feature/catalog-service
feature/order-service
feature/payment-service
...
```

### Создание develop ветки

```bash
git checkout main
git checkout -b develop
git push origin develop
```

### Работа с фичами

```bash
# Создание фичи от develop
git checkout develop
git checkout -b feature/your-feature

# После завершения
git checkout develop
git merge feature/your-feature
git push origin develop

# Когда develop готов к релизу
git checkout main
git merge develop
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main --tags
```

## 📚 Полезные Git команды

### Просмотр истории

```bash
# Красивый лог
git log --oneline --graph --all --decorate

# Изменения в файле
git log -p <file>

# Кто и когда менял строки
git blame <file>
```

### Отмена изменений

```bash
# Отменить изменения в файле
git checkout -- <file>

# Отменить последний коммит (сохранив изменения)
git reset --soft HEAD~1

# Отменить последний коммит (удалив изменения)
git reset --hard HEAD~1

# Исправить последний коммит
git commit --amend
```

### Работа с ветками

```bash
# Список всех веток
git branch -a

# Удалить локальную ветку
git branch -d feature/old-feature

# Удалить удалённую ветку
git push origin --delete feature/old-feature

# Переименовать ветку
git branch -m old-name new-name
```

### Синхронизация

```bash
# Получить изменения без merge
git fetch origin

# Получить изменения с merge
git pull origin main

# Rebase вместо merge
git pull --rebase origin main
```

## 📋 Checklist перед первым push

- [ ] Создан репозиторий на GitHub
- [ ] Файл `.env` добавлен в `.gitignore`
- [ ] Все конфиденциальные данные удалены из кода
- [ ] README.md заполнен
- [ ] GETTING_STARTED.md содержит актуальные инструкции
- [ ] Docker Compose файлы проверены
- [ ] Структура проекта соответствует плану
- [ ] Комментарии в коде написаны на русском языке
- [ ] API документация доступна через Swagger

## 🎯 Готово к push!

Выполните команды из **Шага 3** и ваш проект будет загружен на GitHub!

```bash
git add .
git commit -m "🎉 Initial commit: Project structure and Catalog Service"
git push -u origin main
```

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте, что Git установлен: `git --version`
2. Проверьте авторизацию на GitHub
3. Убедитесь, что SSH ключ добавлен (для SSH) или используйте HTTPS
4. Проверьте права доступа к репозиторию

---

**Следующий шаг**: После успешного push переходите к разработке следующего микросервиса (Order Service) согласно плану в README.md