# 🗄️ MySQL Migration Guide

## Overview

This guide will help you migrate your SmartFitStudios project from SQLite to MySQL database.

---

## 📋 Prerequisites

### 1. Install MySQL Server

#### Windows
1. **Download MySQL Installer:**
   - Visit: https://dev.mysql.com/downloads/installer/
   - Download MySQL Installer for Windows

2. **Run Installer:**
   - Choose "Developer Default" or "Server only"
   - Set root password (remember this!)
   - Complete installation

3. **Verify Installation:**
```bash
mysql --version
```

#### Mac
```bash
brew install mysql
brew services start mysql
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 2. Install MySQL Client for Python

```bash
pip install mysqlclient
```

**If you get errors on Windows:**
```bash
# Alternative: Use PyMySQL
pip install pymysql
```

---

## 🚀 Step-by-Step Migration

### Step 1: Create MySQL Database

#### Option A: Using MySQL Command Line

1. **Login to MySQL:**
```bash
mysql -u root -p
```

2. **Create Database:**
```sql
CREATE DATABASE smartfitstudios_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. **Create User (Optional but Recommended):**
```sql
CREATE USER 'smartfit_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON smartfitstudios_db.* TO 'smartfit_user'@'localhost';
FLUSH PRIVILEGES;
```

4. **Exit:**
```sql
EXIT;
```

#### Option B: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Click "Create New Schema"
4. Name: `smartfitstudios_db`
5. Charset: `utf8mb4`
6. Collation: `utf8mb4_unicode_ci`
7. Click "Apply"

---

### Step 2: Update .env File

Add MySQL configuration to your `.env` file:

```env
# Database Configuration
DB_ENGINE=mysql
DB_NAME=smartfitstudios_db
DB_USER=smartfit_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306
```

**Full .env example:**
```env
# Django Secret Key
SECRET_KEY=your-secret-key-here

# Google Gemini API Key
GEMINI_API_KEY=AIzaSyDktTtX2nXl-QTBWuLmZho5fV3PzDS9d9A

# n8n Webhook URL
N8N_VIDEO_WEBHOOK_URL=http://localhost:5678/webhook/video-vton

# Debug Mode
DEBUG=True

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_ENGINE=mysql
DB_NAME=smartfitstudios_db
DB_USER=smartfit_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306
```

---

### Step 3: Update settings.py

Replace the DATABASES configuration in `greatkart/settings.py`:

**Find this (around line 80):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Replace with:**
```python
# Database Configuration
DB_ENGINE = config('DB_ENGINE', default='sqlite')

if DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    # Fallback to SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

---

### Step 4: Update requirements.txt

Add MySQL client:

```txt
mysqlclient==2.2.0
```

**Or if using PyMySQL:**
```txt
pymysql==1.1.0
```

**If using PyMySQL, also add to settings.py (at the top):**
```python
import pymysql
pymysql.install_as_MySQLdb()
```

---

### Step 5: Run Migrations

1. **Test Database Connection:**
```bash
python manage.py check
```

2. **Create Tables:**
```bash
python manage.py migrate
```

3. **Create Superuser:**
```bash
python manage.py createsuperuser
```

---

### Step 6: Export Data from SQLite (Optional)

If you have existing data in SQLite:

#### Method 1: Using dumpdata/loaddata

1. **Export from SQLite:**
```bash
# Make sure you're using SQLite in settings
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > data_backup.json
```

2. **Switch to MySQL** (update .env)

3. **Run migrations:**
```bash
python manage.py migrate
```

4. **Import data:**
```bash
python manage.py loaddata data_backup.json
```

#### Method 2: Manual Export/Import

For specific apps:
```bash
# Export
python manage.py dumpdata accounts > accounts_data.json
python manage.py dumpdata store > store_data.json
python manage.py dumpdata carts > carts_data.json

# Import (after switching to MySQL)
python manage.py loaddata accounts_data.json
python manage.py loaddata store_data.json
python manage.py loaddata carts_data.json
```

---

## 🔧 Troubleshooting

### Issue: "mysqlclient installation failed"

**Windows Solution:**
```bash
# Install Visual C++ Build Tools first
# Then try:
pip install mysqlclient

# Or use PyMySQL instead:
pip install pymysql
```

**Add to settings.py if using PyMySQL:**
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Issue: "Access denied for user"

**Solution:** Check credentials in .env
```env
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
```

### Issue: "Can't connect to MySQL server"

**Solution:** 
1. Check MySQL is running:
```bash
# Windows
net start MySQL80

# Mac
brew services start mysql

# Linux
sudo systemctl start mysql
```

2. Check host and port in .env:
```env
DB_HOST=localhost
DB_PORT=3306
```

### Issue: "Unknown database"

**Solution:** Create the database first:
```sql
CREATE DATABASE smartfitstudios_db;
```

### Issue: "Character set issues"

**Solution:** Ensure utf8mb4:
```python
'OPTIONS': {
    'charset': 'utf8mb4',
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
},
```

---

## 📊 Verification

### Check Database Connection

```bash
python manage.py dbshell
```

Should open MySQL prompt:
```
mysql>
```

### Check Tables

```sql
SHOW TABLES;
```

Should list all Django tables.

### Check Data

```sql
SELECT * FROM accounts_account LIMIT 5;
```

---

## 🎯 Configuration Summary

### .env File
```env
DB_ENGINE=mysql
DB_NAME=smartfitstudios_db
DB_USER=smartfit_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306
```

### settings.py
```python
from decouple import config

DB_ENGINE = config('DB_ENGINE', default='sqlite')

if DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### requirements.txt
```txt
mysqlclient==2.2.0
# or
pymysql==1.1.0
```

---

## 🔄 Switching Between Databases

You can easily switch between SQLite and MySQL:

### Use MySQL
```env
DB_ENGINE=mysql
```

### Use SQLite
```env
DB_ENGINE=sqlite
```

Then restart Django server.

---

## 🎓 Best Practices

### 1. Backup Regularly

```bash
# Backup MySQL database
mysqldump -u smartfit_user -p smartfitstudios_db > backup_$(date +%Y%m%d).sql

# Restore
mysql -u smartfit_user -p smartfitstudios_db < backup_20250112.sql
```

### 2. Use Different Databases for Dev/Prod

**.env.development:**
```env
DB_ENGINE=sqlite
```

**.env.production:**
```env
DB_ENGINE=mysql
DB_NAME=smartfitstudios_prod
```

### 3. Connection Pooling (Production)

```python
'OPTIONS': {
    'charset': 'utf8mb4',
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    'connect_timeout': 10,
},
'CONN_MAX_AGE': 600,  # Connection pooling
```

### 4. Read Replicas (Advanced)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smartfitstudios_db',
        # ... primary database
    },
    'replica': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smartfitstudios_db',
        # ... read replica
    }
}
```

---

## 📝 Quick Command Reference

### MySQL Commands

```sql
-- Show databases
SHOW DATABASES;

-- Use database
USE smartfitstudios_db;

-- Show tables
SHOW TABLES;

-- Describe table
DESCRIBE accounts_account;

-- Show table size
SELECT 
    table_name AS 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'smartfitstudios_db';
```

### Django Commands

```bash
# Check database
python manage.py dbshell

# Show migrations
python manage.py showmigrations

# Run migrations
python manage.py migrate

# Create migration
python manage.py makemigrations

# SQL for migration
python manage.py sqlmigrate accounts 0001
```

---

## ✅ Migration Checklist

### Pre-Migration
- [ ] Install MySQL Server
- [ ] Install mysqlclient or pymysql
- [ ] Create MySQL database
- [ ] Create MySQL user
- [ ] Update .env file
- [ ] Update settings.py
- [ ] Backup SQLite data (if needed)

### Migration
- [ ] Test database connection
- [ ] Run migrations
- [ ] Import data (if needed)
- [ ] Create superuser
- [ ] Test application

### Post-Migration
- [ ] Verify all tables created
- [ ] Check data integrity
- [ ] Test all features
- [ ] Update documentation
- [ ] Backup MySQL database

---

## 🎉 Success!

Once completed, your SmartFitStudios will be running on MySQL! 🎊

### Benefits of MySQL

- ✅ **Better Performance**: Faster for large datasets
- ✅ **Scalability**: Handles more concurrent users
- ✅ **Production Ready**: Industry standard
- ✅ **Advanced Features**: Full-text search, replication
- ✅ **Better Concurrency**: Multiple connections

---

**Version**: 1.0.0  
**Status**: Complete Guide ✅  
**Database**: MySQL Migration 🗄️
