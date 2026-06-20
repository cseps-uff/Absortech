#!/bin/sh
set -e

is_true() {
    case "$1" in
        1|true|True|TRUE|yes|Yes|YES) return 0 ;;
        *) return 1 ;;
    esac
}

# Map POSTGRES_* variables to DB_* if they exist (Railway compatibility)
export DB_NAME="${DB_NAME:-$POSTGRES_DB}"
export DB_USER="${DB_USER:-$POSTGRES_USER}"
export DB_PASSWORD="${DB_PASSWORD:-$POSTGRES_PASSWORD}"
export DB_HOST="${DB_HOST:-$POSTGRES_HOST}"
export DB_PORT="${DB_PORT:-$POSTGRES_PORT}"

echo "Running migrate..."
python manage.py migrate --noinput

if is_true "${DJANGO_RUNSERVER:-$DJANGO_DEBUG}"; then
    echo "Initializing Django development server..."
    exec python manage.py runserver 0.0.0.0:${PORT:-8000}
fi

echo "Collecting statics..."
python manage.py collectstatic --noinput

echo "Initializing Gunicorn..."
exec python -m gunicorn DjangoAbsortech.wsgi:application \
     --bind 0.0.0.0:${PORT:-8000} \
     --workers ${GUNICORN_WORKERS:-3} \
     --threads ${GUNICORN_THREADS:-3} \
     --timeout 30
