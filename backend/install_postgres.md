# PostgreSQL Installation Guide

## Option 1: Download PostgreSQL Installer
1. Go to https://www.postgresql.org/download/windows/
2. Download PostgreSQL 15 or 16
3. Run installer and set password for 'postgres' user
4. Remember the port (default: 5432)

## Option 2: Use Docker (if you have Docker installed)
```bash
docker run --name joblink-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=joblink -p 5432:5432 -d postgres:15
```

## After Installation:
1. Open pgAdmin or command line
2. Create database named 'joblink'
3. Update .env file with your database credentials