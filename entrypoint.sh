#!/bin/sh

set -e

# Ждём пока PostgreSQL будет готов
echo "Waiting for PostgreSQL..."
while ! python -c "import socket; s = socket.socket(); s.connect(('db', 5432)); s.close()" 2>/dev/null; do
    sleep 1
done
echo "PostgreSQL started!"

# Применяем миграции при запуске сервера
if [ "$1" = "python" ] && [ "$2" = "manage.py" ] && [ "$3" = "runserver" ]; then
    echo "Make migrations..."
    python manage.py makemigrations --noinput
    echo "Applying migrations..."
    python manage.py migrate --noinput
fi

exec "$@"