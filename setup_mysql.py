#!/usr/bin/env python
"""
MySQL Setup Helper Script for SmartFitStudios
This script helps you set up MySQL database configuration
"""

import os
import sys

def main():
    print("=" * 60)
    print("SmartFitStudios - MySQL Setup Helper")
    print("=" * 60)
    print()
    
    print("This script will help you configure MySQL for your project.")
    print()
    
    # Get database details
    print("Please provide your MySQL database details:")
    print()
    
    db_name = input("Database Name [smartfitstudios_db]: ").strip() or "smartfitstudios_db"
    db_user = input("Database User [smartfit_user]: ").strip() or "smartfit_user"
    db_password = input("Database Password: ").strip()
    
    if not db_password:
        print("Error: Password cannot be empty!")
        sys.exit(1)
    
    db_host = input("Database Host [localhost]: ").strip() or "localhost"
    db_port = input("Database Port [3306]: ").strip() or "3306"
    
    print()
    print("-" * 60)
    print("Configuration Summary:")
    print("-" * 60)
    print(f"Database Name: {db_name}")
    print(f"Database User: {db_user}")
    print(f"Database Password: {'*' * len(db_password)}")
    print(f"Database Host: {db_host}")
    print(f"Database Port: {db_port}")
    print("-" * 60)
    print()
    
    confirm = input("Is this correct? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        print("Setup cancelled.")
        sys.exit(0)
    
    # Update .env file
    env_path = '.env'
    
    if not os.path.exists(env_path):
        print(f"Error: {env_path} file not found!")
        sys.exit(1)
    
    # Read current .env
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Update or add database configuration
    db_config = {
        'DB_ENGINE': 'mysql',
        'DB_NAME': db_name,
        'DB_USER': db_user,
        'DB_PASSWORD': db_password,
        'DB_HOST': db_host,
        'DB_PORT': db_port,
    }
    
    # Remove existing DB_ lines
    lines = [line for line in lines if not line.startswith('DB_')]
    
    # Add new configuration
    lines.append('\n# Database Configuration (MySQL)\n')
    for key, value in db_config.items():
        lines.append(f'{key}={value}\n')
    
    # Write back to .env
    with open(env_path, 'w') as f:
        f.writelines(lines)
    
    print()
    print("✅ .env file updated successfully!")
    print()
    print("Next steps:")
    print("1. Install MySQL client: pip install mysqlclient")
    print("2. Create MySQL database:")
    print(f"   mysql -u root -p")
    print(f"   CREATE DATABASE {db_name};")
    print(f"   CREATE USER '{db_user}'@'localhost' IDENTIFIED BY 'your_password';")
    print(f"   GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost';")
    print(f"   FLUSH PRIVILEGES;")
    print(f"   EXIT;")
    print("3. Run migrations: python manage.py migrate")
    print("4. Create superuser: python manage.py createsuperuser")
    print()
    print("See MYSQL_MIGRATION_GUIDE.md for detailed instructions.")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
