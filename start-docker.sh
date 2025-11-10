#!/bin/bash

# WealthWise Docker Quick Start Script
# This script helps you get started with Docker quickly

echo "🚀 WealthWise Portfolio Tracker - Docker Setup"
echo "=============================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running!"
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is installed and running"
echo ""

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed!"
    echo "Please install docker-compose or use Docker Desktop which includes it."
    exit 1
fi

echo "✅ docker-compose is available"
echo ""

# Clean up any existing containers and volumes
echo "🧹 Cleaning up existing containers..."
docker-compose down -v 2>/dev/null || true

echo ""
# Start services
echo "📦 Starting all services (PostgreSQL + Redis + FastAPI)..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
echo "   (This may take 30-40 seconds on first run)"
sleep 15

# Wait for postgres to be ready
echo "   ⌛ Waiting for PostgreSQL..."
until docker exec wealthwise-db pg_isready -U postgres -d wealthwise > /dev/null 2>&1; do
    sleep 2
done
echo "   ✅ PostgreSQL is ready"

# Check if database tables exist, if not initialize
echo "   🔍 Checking database initialization..."
TABLE_COUNT=$(docker exec wealthwise-db psql -U postgres -d wealthwise -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null | tr -d ' ')

if [ "$TABLE_COUNT" -eq "0" ]; then
    echo "   📥 Initializing database with schema and sample data..."
    docker exec -i wealthwise-db psql -U postgres -d wealthwise < setup.sql > /dev/null 2>&1
    echo "   ✅ Database initialized successfully"
else
    echo "   ✅ Database already initialized ($TABLE_COUNT tables found)"
fi

# Wait for app to be ready
echo "   ⌛ Waiting for FastAPI app..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🔍 Testing API connection..."
sleep 5

# Test API
if curl -s http://localhost:8000/prices > /dev/null; then
    echo "✅ API is running successfully!"
else
    echo "⚠️  API might still be starting. Check logs with: docker-compose logs -f app"
fi

echo ""
echo "=============================================="
echo "🎉 Setup Complete!"
echo ""
echo "📍 Access Points:"
echo "   • API:        http://localhost:8000"
echo "   • Swagger UI: http://localhost:8000/docs"
echo "   • PostgreSQL: localhost:5432"
echo "   • Redis:      localhost:6379"
echo ""
echo "📝 Quick Commands:"
echo "   • View logs:     docker-compose logs -f app"
echo "   • Stop all:      docker-compose down"
echo "   • Restart:       docker-compose restart"
echo ""
echo "🧪 Test the API:"
echo "   curl http://localhost:8000/prices"
echo ""
