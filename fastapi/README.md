# skill-tree

## Запуск
1. Запустить скрипт командой из папки fastapi: `sh ./bashscripts/start.sh`

## Подключение к pgAdmin
1. Открыть localhost:<порт pgAdmin из .env>
2. Войти по логину и паролю из .env
3. Зарегистрировать сервер со следующими параметрами:
    - Host name/address: postgres
    - Port: 5432
    - Maintenance database: <название бд из .env>
    - Username: <пользователь из .env>
    - Password: <пароль из .env>

## Управление миграциями с alembic
1. Создать миграцию
    - docker compose exec fastapi alembic revision --autogenerate -m "<comment>"
2. Применить последнюю миграцию
    - docker compose exec fastapi alembic upgrade head
3. Применить конкретную миграцию
    - docker compose exec fastapi alembic upgrade / downgrade <revision identifier>
