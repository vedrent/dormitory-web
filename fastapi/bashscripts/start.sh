#!/bin/bash

ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Создаем .env файл..."
    
    echo "FASTAPI_PORT=6981" >> "$ENV_FILE"
    echo "JWT_SECRET_KEY=d_-AbS6mp1yOUPH2x7Xbf2fzTNU-9vB6jqiK-1LidrE" >> "$ENV_FILE"
    echo "JWT_REFRESH_SECRET_KEY=RJy8QV0LjSsWANcfO9kC8XJZL4bfwtFwj3L1JW4ZDwo" >> "$ENV_FILE"

    echo "POSTGRES_DB=postgres_db" >> "$ENV_FILE"
    echo "POSTGRES_USER=postgres_user" >> "$ENV_FILE"
    echo "POSTGRES_PASSWORD=postgres_password" >> "$ENV_FILE"

    echo "PGADMIN_PORT=6982" >> "$ENV_FILE"
    echo "PGADMIN_DEFAULT_EMAIL=admin@admin.ru" >> "$ENV_FILE"
    echo "PGADMIN_DEFAULT_PASSWORD=password" >> "$ENV_FILE"


    echo ".env файл создан."
fi

docker compose --env-file .env up -d --build