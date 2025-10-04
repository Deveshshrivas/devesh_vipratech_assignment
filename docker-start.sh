echo "Django E-Commerce Docker Setup"
echo "=================================="

if ! command -v docker &> /dev/null; then
    echo " Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "Docker and Docker Compose are installed"
echo ""

# Ask user for setup type
echo "Choose setup type:"
echo "1) Simple (SQLite) - Recommended for testing"
echo "2) Full (PostgreSQL) - Complete setup"
echo "3) Production - With Nginx and Gunicorn"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting simple Docker setup with SQLite..."
        docker-compose -f docker-compose.simple.yml up --build
        ;;
    2)
        echo ""
        echo "🚀 Starting full Docker setup with PostgreSQL..."
        docker-compose up --build
        ;;
    3)
        echo ""
        echo "⚠️  Production setup requires .env.prod file"
        if [ ! -f .env.prod ]; then
            echo "Creating .env.prod from template..."
            cp .env.prod.example .env.prod
            echo "⚠️  Please edit .env.prod with your production values!"
            echo "Press Enter to continue after editing..."
            read
        fi
        echo "🚀 Starting production Docker setup..."
        docker-compose -f docker-compose.prod.yml up --build -d
        echo ""
        echo "✅ Production containers started in background"
        echo "📊 Check status: docker-compose -f docker-compose.prod.yml ps"
        echo "📋 View logs: docker-compose -f docker-compose.prod.yml logs -f"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
