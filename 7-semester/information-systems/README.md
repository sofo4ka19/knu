# Моніторинг роботи з базою даних

Навчальна інформаційна система інтернет-магазину. Програма-генератор постійно створює, змінює й видаляє дані в PostgreSQL, а навколо неї працює стек спостережуваності: метрики (Prometheus), логи (Loki) і трейси (Tempo), які об'єднує Grafana. Усі зміни даних проходять через чергу RabbitMQ. Доступ до системи мають лише авторизовані користувачі.

## Архітектура

```
браузер ──► nginx (:8080) ──auth_request──► auth (Flask + SQLite)
              │ сесія дійсна
              ├──► Grafana ──► Prometheus ◄── generator, consumer,
              │       │                       postgres_exporter, rabbitmq
              │       ├──► Loki  ◄── Promtail ◄── логи контейнерів
              │       └──► Tempo ◄── OTLP ◄── generator, consumer
              └──► Prometheus UI (/prometheus/)

generator ──події──► RabbitMQ ──► consumer ──► PostgreSQL
generator ──звіти (читання)──────────────────► PostgreSQL
```

Записи йдуть через чергу, читання напряму. Генератор лише публікує подію («створити замовлення», «змінити статус»), а `consumer` виконує її в базі.

## Запуск

Потрібен Docker Desktop (або Docker Engine з Compose).

```bash
cp .env.example .env        # Windows (PowerShell): copy .env.example .env
docker compose up -d --build
docker compose ps
```

У `.env` замініть значення `change_me` на власні паролі. Перший запуск триває кілька хвилин. Через 2-3 хвилини відкрийте http://localhost:8080 і увійдіть із `AUTH_ADMIN_USER` та `AUTH_ADMIN_PASSWORD`. Перші точки на графіках з'являються через 1-2 хвилини.

Зупинити: `docker compose down`. Видалити разом з даними: `docker compose down -v`.

## Змінні середовища

Файл `.env` у git не потрапляє, у репозиторії лежить шаблон `.env.example`:

```
POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB    база даних
DB_PORT                                          порт бази для локального запуску
GRAFANA_ADMIN_USER, GRAFANA_ADMIN_PASSWORD       адміністратор Grafana
AUTH_ADMIN_USER, AUTH_ADMIN_PASSWORD             перший користувач системи
RABBITMQ_USER, RABBITMQ_PASSWORD                 доступ до RabbitMQ
```

## Куди заходити

- http://localhost:8080 — Grafana з дашбордом
- http://localhost:8080/prometheus/ — Prometheus, сторінка `Status → Targets` показує, чи всі джерела метрик працюють (мають бути UP)

Назовні відкрито один порт, 8080 (Nginx). Grafana, Prometheus і сервер авторизації напряму недоступні, тому авторизацію не можна обійти.

## Користувачі

```bash
docker compose exec auth python manage.py adduser ivan
docker compose exec auth python manage.py passwd ivan
docker compose exec auth python manage.py list
```

## Структура

```
docker-compose.yml     усі сервіси
.env.example           шаблон змінних
generator/             генератор даних (Python)
consumer/              споживач черги, запис у PostgreSQL (Python)
auth/                  сервер авторизації (Flask + SQLite)
nginx/                 єдина точка входу
prometheus/            цілі збору метрик
loki/  promtail/       зберігання та збір логів
tempo/                 зберігання трейсів
grafana/               джерела даних і дашборд
```

## Примітки

- Помилки `duplicate key ... customers_email_key` у логах природні: після перезапуску генератор може повторити email, який уже є в базі.
- Час у тексті логів за UTC, Grafana показує час браузера.
