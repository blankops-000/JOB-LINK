#!/bin/bash
# Deployment script for JobLink backend

echo "🚀 Starting JobLink Backend Deployment..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️ Running database migrations..."
flask db upgrade

echo "✅ Deployment complete!"