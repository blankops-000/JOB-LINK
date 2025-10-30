# 🗄️ SQLite Database Setup - JobLink

## ✅ Database Successfully Created!

**Location:** `backend/instance/joblink.db`  
**Type:** SQLite3  
**Size:** ~64 KB  
**Status:** Ready to use

---

## 📊 Database Configuration

### Current Setup (in `.env`):
```env
DATABASE_URL=sqlite:///joblink.db
```

This creates the database at: `backend/instance/joblink.db`

---

## 🔧 Manual Database Management

### 1. **View Database Tables**
```bash
cd backend
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('\n'.join(db.engine.table_names()))"
```

### 2. **Recreate Database (Fresh Start)**
```bash
cd backend
rm -f instance/joblink.db
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Database recreated')"
```

### 3. **Check Database Size**
```bash
ls -lh backend/instance/joblink.db
```

### 4. **Backup Database**
```bash
cp backend/instance/joblink.db backend/instance/joblink_backup_$(date +%Y%m%d).db
```

### 5. **View Database with SQLite Browser**
```bash
# Install sqlite3 browser
sudo apt install sqlitebrowser

# Open database
sqlitebrowser backend/instance/joblink.db
```

---

## 📋 Database Tables

Your database includes these tables:

1. **users** - User accounts (clients, providers, admins)
2. **provider_profiles** - Provider business profiles
3. **service_categories** - Service types (plumbing, electrical, etc.)
4. **bookings** - Service bookings/appointments
5. **reviews** - Customer reviews and ratings
6. **payments** - Payment transactions (M-Pesa)
7. **alembic_version** - Migration tracking

---

## 🔄 Using Migrations (Recommended for Production)

### Initialize Migrations (if needed):
```bash
cd backend
flask db init
```

### Create Migration After Model Changes:
```bash
flask db migrate -m "Description of changes"
```

### Apply Migrations:
```bash
flask db upgrade
```

### Rollback Migration:
```bash
flask db downgrade
```

---

## 🚨 Common Issues & Solutions

### Issue 1: "Table already exists"
**Solution:** Drop and recreate
```bash
cd backend
rm instance/joblink.db
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### Issue 2: "Database is locked"
**Solution:** Stop all Flask servers
```bash
lsof -ti:5000 | xargs kill -9
```

### Issue 3: "Migration conflicts"
**Solution:** Reset migrations
```bash
cd backend
rm -rf migrations/versions/*.py
flask db stamp head
flask db migrate -m "Reset migrations"
flask db upgrade
```

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(10) NOT NULL,  -- 'client', 'provider', 'admin'
    is_verified BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Provider Profiles Table
```sql
CREATE TABLE provider_profiles (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    business_name VARCHAR(100),
    description TEXT,
    service_category_id INTEGER,
    location VARCHAR(200),
    latitude FLOAT,
    longitude FLOAT,
    hourly_rate FLOAT,
    availability TEXT,
    profile_image VARCHAR(500),
    average_rating FLOAT,
    review_count INTEGER DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (service_category_id) REFERENCES service_categories(id)
);
```

### Bookings Table
```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    provider_id INTEGER NOT NULL,
    service_category_id INTEGER,
    booking_date DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    location VARCHAR(200),
    description TEXT,
    estimated_cost FLOAT,
    actual_cost FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES users(id),
    FOREIGN KEY (provider_id) REFERENCES users(id),
    FOREIGN KEY (service_category_id) REFERENCES service_categories(id)
);
```

### Reviews Table
```sql
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    booking_id INTEGER UNIQUE NOT NULL,
    client_id INTEGER NOT NULL,
    provider_id INTEGER NOT NULL,
    provider_profile_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id),
    FOREIGN KEY (client_id) REFERENCES users(id),
    FOREIGN KEY (provider_id) REFERENCES users(id),
    FOREIGN KEY (provider_profile_id) REFERENCES provider_profiles(id)
);
```

### Payments Table
```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    booking_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    payment_method VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    mpesa_receipt VARCHAR(100),
    transaction_id VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);
```

---

## 🔐 Database Security

### For Development (Current):
- ✅ SQLite is fine
- ✅ Database file is gitignored
- ✅ No password needed

### For Production:
Switch to PostgreSQL in `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/joblink_prod
```

---

## 📈 Database Maintenance

### Regular Backups:
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp backend/instance/joblink.db "backups/joblink_$DATE.db"
echo "✅ Backup created: joblink_$DATE.db"
```

### Vacuum Database (Optimize):
```bash
sqlite3 backend/instance/joblink.db "VACUUM;"
```

### Check Database Integrity:
```bash
sqlite3 backend/instance/joblink.db "PRAGMA integrity_check;"
```

---

## ✅ Your Database is Ready!

- **Location:** `backend/instance/joblink.db`
- **All tables created:** ✅
- **Ready for signup/login:** ✅
- **M-Pesa payments:** ✅
- **Reviews & ratings:** ✅
- **Geo-location:** ✅

**No need to worry about database issues anymore!** 🎉
