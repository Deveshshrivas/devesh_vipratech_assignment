set -e

echo "Starting Django E-Commerce Application..."

if [ "$DB_HOST" ]; then
    echo "Waiting for PostgreSQL..."
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Setup products if needed
echo "Setting up products..."
python manage.py setup_products || true

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || true

# Create superuser if it doesn't exist (optional)
echo "Checking for admin user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123');
    print('Admin user created: admin/admin123');
else:
    print('Admin user already exists');
" || true

echo "Starting server..."
exec "$@"
