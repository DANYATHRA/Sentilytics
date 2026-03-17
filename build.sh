#!/usr/bin/env bash
set -o errexit

echo "Installing dependencies..."
cd backend
pip install -r requirements.txt

echo "Creating static directories..."
mkdir -p staticfiles

echo "Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true

echo "Running migrations..."
python manage.py migrate --noinput

echo "Build complete!"
