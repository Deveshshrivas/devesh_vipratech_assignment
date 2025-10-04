# Quick Docker Setup Script for Windows PowerShell

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Django E-Commerce Docker Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    docker --version | Out-Null
    Write-Host "✅ Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "Visit: https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Yellow
    exit 1
}

# Check if Docker Compose is installed
try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose is not installed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Choose setup type:" -ForegroundColor Yellow
Write-Host "1) Simple (SQLite) - Recommended for testing"
Write-Host "2) Full (PostgreSQL) - Complete setup"
Write-Host "3) Production - With Nginx and Gunicorn"
Write-Host ""

$choice = Read-Host "Enter choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🚀 Starting simple Docker setup with SQLite..." -ForegroundColor Green
        docker-compose -f docker-compose.simple.yml up --build
    }
    "2" {
        Write-Host ""
        Write-Host "🚀 Starting full Docker setup with PostgreSQL..." -ForegroundColor Green
        docker-compose up --build
    }
    "3" {
        Write-Host ""
        Write-Host "⚠️  Production setup requires .env.prod file" -ForegroundColor Yellow
        
        if (-not (Test-Path .env.prod)) {
            Write-Host "Creating .env.prod from template..." -ForegroundColor Yellow
            Copy-Item .env.prod.example .env.prod
            Write-Host "⚠️  Please edit .env.prod with your production values!" -ForegroundColor Red
            Write-Host "Press Enter to continue after editing..." -ForegroundColor Yellow
            Read-Host
        }
        
        Write-Host "🚀 Starting production Docker setup..." -ForegroundColor Green
        docker-compose -f docker-compose.prod.yml up --build -d
        
        Write-Host ""
        Write-Host "✅ Production containers started in background" -ForegroundColor Green
        Write-Host "📊 Check status: docker-compose -f docker-compose.prod.yml ps" -ForegroundColor Cyan
        Write-Host "📋 View logs: docker-compose -f docker-compose.prod.yml logs -f" -ForegroundColor Cyan
    }
    default {
        Write-Host "❌ Invalid choice" -ForegroundColor Red
        exit 1
    }
}
