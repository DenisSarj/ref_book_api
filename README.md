# Ref Book Service

Ref Book Service — это REST API сервис на FastAPI для работы со справочником организаций, зданий и видов деятельности. Поддерживает поиск организаций по радиусу и вложенные виды деятельности.

## Deployment

### 1. Создайте файл окружения

Создайте `.env` в корне проекта, используя `env.example` в качестве примера:
```sh
cp env.example .env
```

### 2. Запустите сервисы через Docker Compose
```sh
docker compose up -d --build
```

### 3. Подключитесь к контейнеру
```sh
docker exec -it ref-book-svc bash
```

### 4. Выполните миграции
```sh
alembic -c src/alembic.ini upgrade head
```

### 5. Заполните базу тестовыми данными
```sh
python infra/helpers/load_test_data.py
```

Теперь сервис готов к использованю)

