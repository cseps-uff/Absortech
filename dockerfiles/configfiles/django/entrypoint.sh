#!/bin/sh
set -e

echo "Running migrate..."
python manage.py migrate --noinput

echo "Collecting statics..."
python manage.py collectstatic --noinput

echo "Initializing Gunicorn..."
exec python -m gunicorn DjangoAbsortech.wsgi:application \\
     --bind 0.0.0.0:${PORT:-8000} \\
     --workers ${GUNICORN_WORKERS:-3} \
     --threads ${GUNICORN_THREADS:-3} \
     --timeout 30
