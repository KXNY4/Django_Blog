# DRF Mini Blog

REST API для блог-платформы на Django REST Framework.

## Технологический стек

- **Python** 3.12
- **Django** 6.0
- **Django REST Framework** 3.16
- **PostgreSQL** 17
- **Docker** + **Docker Compose**
- **SimpleJWT** — аутентификация
- **drf-spectacular** — Swagger/OpenAPI документация
- **django-filter** — фильтрация
- **pytest** — тестирование

## Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone <url>
cd drf_mini_blog
```

### 2. Создайте файл переменных окружения

```bash
cp .envs/dev.env.example .envs/dev.env
```

Пример `.envs/dev.env`:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=drf_mini_blog
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 3. Запустите проект

```bash
cd Docker
docker-compose up --build
```

Миграции применяются автоматически при старте.

### 4. Создайте суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

## API Endpoints

### Аутентификация

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| POST | `/api/auth/register/` | Регистрация | Public |
| POST | `/api/auth/login/` | Вход (получение JWT токенов) | Public |
| POST | `/api/auth/logout/` | Выход (blacklist refresh token) | Auth |
| POST | `/api/auth/token/refresh/` | Обновление access токена | Public |

### Пользователи

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/users/profile/me/` | Мой профиль | Auth |
| PATCH | `/api/users/profile/me/` | Редактировать профиль | Auth |
| GET | `/api/users/profile/{id}/` | Публичный профиль | Public |

### Посты

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/posts/` | Список постов | Public |
| POST | `/api/posts/` | Создать пост | Auth |
| GET | `/api/posts/{slug}/` | Детали поста | Public |
| PATCH | `/api/posts/{slug}/` | Редактировать пост | Owner |
| DELETE | `/api/posts/{slug}/` | Удалить пост | Owner |
| GET | `/api/posts/my/` | Мои посты | Auth |
| POST | `/api/posts/{slug}/like/` | Лайкнуть пост | Auth |
| DELETE | `/api/posts/{slug}/like/` | Убрать лайк | Auth |

### Комментарии

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/posts/{slug}/comments/` | Комментарии поста | Public |
| POST | `/api/posts/{slug}/comments/` | Добавить комментарий | Auth |
| PATCH | `/api/comments/{id}/` | Редактировать | Owner |
| DELETE | `/api/comments/{id}/` | Удалить | Owner |

### Категории и Теги

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/posts/categories/` | Список категорий | Public |
| GET | `/api/posts/categories/{slug}/` | Детали категории | Public |
| GET | `/api/posts/tags/` | Список тегов | Public |
| GET | `/api/posts/tags/{slug}/` | Детали тега | Public |

### Фильтрация постов

```
GET /api/posts/?category=python
GET /api/posts/?tag=django
GET /api/posts/?author=1
GET /api/posts/?search=текст
GET /api/posts/?ordering=-created_at
```

## Документация API

После запуска доступна по адресам:

- **Swagger UI:** http://localhost:8000/api/schema/swagger-ui/
- **ReDoc:** http://localhost:8000/api/schema/redoc/

## Тестирование

```bash
docker-compose exec web pytest
```

## Структура проекта

```
drf_mini_blog/
├── Docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── apps/
│   ├── core/           # Базовая модель, утилиты
│   ├── users/           # Пользователи, аутентификация
│   ├── posts/           # Посты, категории, теги, лайки
│   └── comments/        # Комментарии
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   └── dev.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── entrypoint.sh
└── pytest.ini
```
