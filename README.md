# Система аутентификации и авторизации

Backend-приложение с собственной системой аутентификации и авторизации на Django REST Framework + PostgreSQL.

## Содержание

- [Установка и запуск](#установка-и-запуск)
- [API Endpoints](#api-endpoints)
  - [Аутентификация](#аутентификация)
  - [Управление доступом](#управление-доступом-только-admin)
  - [Бизнес-объекты](#бизнес-объекты-mock)
- [Архитектура системы доступа](#архитектура-системы-доступа)
- [Схема базы данных](#схема-базы-данных)
- [Тестовые пользователи](#тестовые-пользователи)

## Установка и запуск

```bash
pip install -r requirements.txt

# Создать базу данных PostgreSQL
psql -U postgres -c "CREATE DATABASE auth_system;"

# Настроить подключение в .env (скопировать из .env.example)

python manage.py migrate
python manage.py setup_demo
python manage.py runserver
```

## API Endpoints

### Аутентификация

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/auth/register/` | Регистрация |
| POST | `/api/auth/login/` | Вход |
| POST | `/api/auth/logout/` | Выход |
| GET | `/api/auth/me/` | Текущий пользователь |
| PUT | `/api/auth/me/` | Обновление профиля |
| DELETE | `/api/auth/me/` | Мягкое удаление аккаунта |

### Управление доступом (только admin)

| Метод | URL | Описание |
|-------|-----|----------|
| GET/POST | `/api/access/roles/` | Список/создание ролей |
| GET/PUT/DELETE | `/api/access/roles/{id}/` | Детали роли |
| GET | `/api/access/elements/` | Список бизнес-объектов |
| GET/POST | `/api/access/rules/` | Список/создание правил |
| GET/PUT/DELETE | `/api/access/rules/{id}/` | Детали правила |
| GET/POST | `/api/access/user-roles/` | Роли пользователей |
| DELETE | `/api/access/user-roles/{id}/` | Удаление роли у пользователя |

### Бизнес-объекты (Mock)

| Метод | URL | Описание |
|-------|-----|----------|
| GET/POST | `/api/business/products/` | Товары |
| GET/POST | `/api/business/shops/` | Магазины |
| GET/POST | `/api/business/orders/` | Заказы |

## Архитектура системы доступа

1. **Аутентификация**: JWT токен в заголовке `Authorization: Bearer {token}` или сессия в Cookie
2. **Идентификация**: Middleware проверяет токен/сессию и устанавливает `request.current_user`
3. **Авторизация**: Проверка прав на основе ролей и правил доступа

### Роли

| Роль | Описание |
|------|----------|
| admin | Полный доступ ко всем ресурсам |
| manager | Чтение всех объектов, управление своими |
| user | Управление только своими объектами |
| guest | Только чтение публичных данных |

### Права доступа

- `read_permission` — чтение своих объектов
- `read_all_permission` — чтение всех объектов
- `create_permission` — создание объектов
- `update_permission` — обновление своих объектов
- `update_all_permission` — обновление всех объектов
- `delete_permission` — удаление своих объектов
- `delete_all_permission` — удаление всех объектов

## Схема базы данных

```
users              — пользователи (email, password_hash, ФИО, is_active)
sessions           — сессии (user_id, session_token, expires_at)
roles              — роли (name, description)
user_roles         — связь пользователей и ролей
business_elements  — бизнес-объекты (users, products, shops, orders)
access_rules       — правила доступа (role_id, element_id, *_permission)
```

## Тестовые пользователи

| Email | Пароль | Роль |
|-------|--------|------|
| admin@example.com | admin123 | admin |
| manager@example.com | manager123 | manager |
| user@example.com | user123 | user |
