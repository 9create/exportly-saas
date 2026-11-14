#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
echo "Installing requirements..."
pip install -r requirements.txt

# Collect static files (CSS/JS)
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "Applying migrations..."
python manage.py migrate

# Smart Superuser Creation (Check first, then create)
echo "Checking for superuser..."
if python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0 if User.objects.filter(username='admin').exists() else 1)"; then
    echo "Superuser 'admin' already exists. Skipping creation."
else
    echo "Creating superuser 'admin'..."
    python manage.py createsuperuser --no-input --username admin --email admin@exportly.com
fi