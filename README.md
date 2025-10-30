## DDD Notification Service (Тестовое задание)

Cервис уведомлений c резервной доставкой. Пользователь получает уведомления через Email, SMS и Telegram. Если один канал не сработал — автоматически пробуем следующий.

### Задача (из ТЗ)
- Создать сервис для отправки уведомлений пользователям.
- Каналы: Email, SMS, Telegram.
- Обеспечить надежную доставку: при сбое в одном канале — пробуем другой (fallback).

### Ключевая идея
Уведомление отправляется в worker через очередь задач, одной задачей: «send_notification_with_fallback». В воркере реализован порядок попыток: Email → Telegram → SMS. Как только один канал успешно доставил сообщение — считаем отправку успешной.

---

## Стек

- Python 3.13, FastAPI — REST API
- Pydantic v2, pydantic-settings — схемы и конфигурация
- MongoDB (async motor client) — хранилище пользователей
- Celery — асинхронные задачи
- Redis - брокер для Celery
- punq — DI‑контейнер
- Pytest — тесты

---

## Архитектура (слои и ответственность)

- **Domain (бизнес-модель)**: `app/domain`
  - `entities` — сущности домена, напр. `UserEntity`.
  - `value_objects` — валидируемые значения: `UsernameValueObject`, `EmailValueObject`, `TelegramValueObject`, `PhoneValueObject`.
  - `exceptions` — доменные исключения (ошибки валидации и т.п.).

- **Logic (application layer)**: `app/logic`
  - `use_cases` — сценарии: `CreateUserUseCase` (создаёт пользователя и инициирует отправку уведомления).
  - `services` — прикладные сервисы: `UserService`, `NotificationService` (оборачивает очередь задач, отправляет в worker одну задачу с параметрами пользователя).
  - `mediator` — регистрация и вызов use-case’ов.

- **Infrastructure**: `app/infrastructure`
  - `repositories` — хранение пользователей (MongoDB, in-memory для тестов).
  - `task_queues` — очередь задач: адаптер Celery для продакшена и in-memory очередь для тестов `DummyInMemoryTaskQueue`.

- **Presentation (API)**: `app/presentation/api`
  - FastAPI-приложение, эндпоинт: `POST /user/` — создать пользователя и инициировать отправку уведомления.

---

## Поток данных (коротко)
1) Клиент вызывает `POST /user/` c `username/email/telegram/phone`.
2) Контроллер дергает `CreateUserUseCase` через `Mediator`.
3) Юзер создаётся, затем `NotificationService` отправляет одну задачу в очередь: `send_notification_with_fallback`.
4) Worker берёт задачу и пытается: Email → Telegram → SMS (до успеха).

---

## API

- POST `/api/docs` — swagger UI.

- POST `/user/`
  - Body:
    ```json
    {
      "username": "john_doe",
      "email": "john@example.com",
      "telegram": "@johnny",
      "phone": "+1 (555) 123-4567"
    }
    ```
  - Успех: `201 Created`
    ```json
    {
      "oid": "...",
      "username": "john_doe",
      "email": "john@example.com",
      "telegram": "@johnny",
      "phone": "+1 (555) 123-4567"
    }
    ```
  - Ошибка валидации/логики: `400 Bad Request`
    ```json
    { "detail": { "error": "<человеко-понятное описание>" } }
    ```

---

## Переменные окружения (.env)

Минимальный набор (см. `app/settings/config.py`):

- `MONGO_DB_CONNECTION_URI` — строка подключения к MongoDB
- `MONGODB_USER_DATABASE` — имя БД (по умолчанию `user`)
- `MONGODB_USER_COLLECTION` — коллекция (по умолчанию `user`)
- `REDIS_CONNECTION_URI` — строка подключения Redis (используется для Celery worker)

Для локальной разработки можно оставить значения по умолчанию и поднимать окружение через docker-compose (см. ниже).

---

## Как запустить

Docker Compose

1) Создайте `.env` по примеру `.env.example` и пропишите значения (или оставьте дефолты).
2) Запустите всё:
   ```bash
   make all
   ```
   Это поднимет MongoDB, воркер и приложение.

Полезные команды:
- Остановить всё: `make all-down`
- Только хранилища (MongoDB): `make storages`
- Только приложение: `make app`
- Только очередь/worker: `make task-queue`
- Логи: `make app-logs`, `make celery-logs`, `make storages-logs`

Приложение будет доступно:
- Swagger: `http://localhost:8000/api/docs`

---

## Тесты

Запуск тестов в контейнере приложения:
```bash
make test
```

В тестах DI-контейнер автоматически подменяет:
- Репозиторий пользователей на in-memory реализацию
- Очередь задач на `DummyInMemoryTaskQueue` (без внешних сервисов)
