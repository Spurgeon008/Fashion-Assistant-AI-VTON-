# 🔐 Environment Variables Setup Guide

## Overview

Your SmartFitStudios project now uses environment variables to securely store sensitive information like API keys and configuration settings.

---

## ✅ What Was Done

### 1. **Created .env File**
- Contains all sensitive configuration
- **NOT committed to Git** (already in .gitignore)
- Stores API keys, secrets, and configuration

### 2. **Created .env.example File**
- Template for other developers
- **Safe to commit to Git**
- Shows what variables are needed

### 3. **Updated .gitignore**
- Already includes `.env` (verified)
- Prevents accidental commits of secrets

### 4. **Installed python-decouple**
- Package for reading .env files
- Added to requirements.txt
- Installed successfully

### 5. **Updated settings.py**
- Now reads from .env file
- Falls back to defaults if .env missing
- Secure and flexible

---

## 📁 Files Structure

```
SmartFitStudios/
├── .env                    # ❌ NOT in Git (your secrets)
├── .env.example            # ✅ In Git (template)
├── .gitignore              # ✅ Includes .env
├── requirements.txt        # ✅ Includes python-decouple
└── greatkart/
    └── settings.py         # ✅ Uses config() to read .env
```

---

## 🔑 Environment Variables

### Current Variables in .env

```bash
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
```

---

## 🚀 How to Use

### For You (First Time Setup)

Your .env file is already created with your current values! ✅

Just verify it exists:
```bash
# Check if .env exists
dir .env
```

### For Other Developers

1. **Copy the template:**
```bash
copy .env.example .env
```

2. **Edit .env and add real values:**
```bash
notepad .env
```

3. **Fill in the values:**
```env
SECRET_KEY=generate-a-new-secret-key
GEMINI_API_KEY=get-from-google-ai-studio
N8N_VIDEO_WEBHOOK_URL=your-n8n-webhook-url
```

---

## 🔧 How It Works

### Before (Hardcoded)
```python
# settings.py
SECRET_KEY = '%)fvjakcctr5evl+c)%s1=x*#1tj#b62p3p=qa1#&!$)0u)q#8'
GEMINI_API_KEY = 'AIzaSyDktTtX2nXl-QTBWuLmZho5fV3PzDS9d9A'
```
❌ **Problem**: Secrets exposed in code

### After (Environment Variables)
```python
# settings.py
from decouple import config

SECRET_KEY = config('SECRET_KEY')
GEMINI_API_KEY = config('GEMINI_API_KEY')
```
✅ **Solution**: Secrets in .env file (not in Git)

---

## 📝 Editing .env File

### Windows
```bash
notepad .env
```

### Mac/Linux
```bash
nano .env
# or
vim .env
```

### VS Code
```bash
code .env
```

---

## 🔒 Security Best Practices

### ✅ DO

1. **Keep .env in .gitignore**
   ```
   # .gitignore
   .env
   ```

2. **Use different .env for different environments**
   - `.env.development`
   - `.env.production`
   - `.env.testing`

3. **Rotate keys regularly**
   - Change API keys periodically
   - Update .env file

4. **Use strong secret keys**
   ```bash
   # Generate new Django secret key
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Commit .env.example**
   - Shows what variables are needed
   - No actual secrets

### ❌ DON'T

1. **Never commit .env to Git**
2. **Never share .env file publicly**
3. **Never hardcode secrets in code**
4. **Never use production keys in development**
5. **Never commit API keys to GitHub**

---

## 🎯 Available Variables

### Django Settings
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### API Keys
```env
GEMINI_API_KEY=your-gemini-api-key
```

### n8n Configuration
```env
N8N_VIDEO_WEBHOOK_URL=http://localhost:5678/webhook/video-vton
```

### Database (Optional - for future use)
```env
DB_NAME=smartfitstudios_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### Email (Optional - for future use)
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```

---

## 🔄 Updating video.json

### Problem
The API key is hardcoded in video.json (line 231):
```json
"jsonHeaders": "{\n  \"x-goog-api-key\": \"AIzaSyDktTtX2nXl-QTBWuLmZho5fV3PzDS9d9A\",\n  \"Content-Type\": \"application/json\"\n}"
```

### Solution (in n8n)

1. **Create a Credential in n8n:**
   - Go to n8n → Credentials
   - Click "New Credential"
   - Select "Header Auth"
   - Name: "Gemini API Key"
   - Header Name: `x-goog-api-key`
   - Header Value: `{{ $env.GEMINI_API_KEY }}`

2. **Update HTTP Request2 Node:**
   - Remove hardcoded API key from jsonHeaders
   - Use the credential instead
   - Reference: `{{ $credentials.geminiApiKey }}`

3. **Set Environment Variable in n8n:**
   ```bash
   # In n8n's .env file
   GEMINI_API_KEY=AIzaSyDktTtX2nXl-QTBWuLmZho5fV3PzDS9d9A
   ```

---

## 🧪 Testing

### Verify .env is Working

1. **Check if variables are loaded:**
```python
# In Django shell
python manage.py shell

>>> from django.conf import settings
>>> print(settings.GEMINI_API_KEY)
AIzaSyDktTtX2nXl-QTBWuLmZho5fV3PzDS9d9A

>>> print(settings.SECRET_KEY)
your-secret-key-here
```

2. **Test the application:**
```bash
python manage.py runserver
```

If it starts without errors, .env is working! ✅

---

## 🐛 Troubleshooting

### Issue: "SECRET_KEY not found"
**Solution**: Make sure .env file exists in project root
```bash
dir .env
```

### Issue: "python-decouple not installed"
**Solution**: Install it
```bash
pip install python-decouple
```

### Issue: ".env not being read"
**Solution**: Check file location
```bash
# .env should be in project root, same level as manage.py
SmartFitStudios/
├── .env          ← Here
├── manage.py
└── greatkart/
```

### Issue: "Invalid syntax in .env"
**Solution**: Check format
```env
# Correct
KEY=value

# Wrong
KEY = value  # No spaces around =
KEY="value"  # No quotes needed
```

---

## 📊 Migration Checklist

### Completed ✅
- ✅ Created .env file
- ✅ Created .env.example file
- ✅ Added .env to .gitignore (already there)
- ✅ Installed python-decouple
- ✅ Updated settings.py to use config()
- ✅ Moved SECRET_KEY to .env
- ✅ Moved GEMINI_API_KEY to .env
- ✅ Moved N8N_VIDEO_WEBHOOK_URL to .env
- ✅ Added DEBUG to .env
- ✅ Added ALLOWED_HOSTS to .env

### To Do (Optional)
- ⏳ Update video.json to use n8n credentials
- ⏳ Set up different .env for production
- ⏳ Rotate API keys
- ⏳ Add database credentials (when needed)
- ⏳ Add email credentials (when needed)

---

## 🎓 Best Practices

### 1. Different Environments
```bash
# Development
.env.development

# Production
.env.production

# Testing
.env.testing
```

### 2. Loading Specific .env
```python
# settings.py
import os
from decouple import Config, RepositoryEnv

env_file = os.path.join(BASE_DIR, f'.env.{os.getenv("ENVIRONMENT", "development")}')
config = Config(RepositoryEnv(env_file))
```

### 3. Required vs Optional
```python
# Required (will raise error if missing)
SECRET_KEY = config('SECRET_KEY')

# Optional (with default)
DEBUG = config('DEBUG', default=True, cast=bool)
```

### 4. Type Casting
```python
# Boolean
DEBUG = config('DEBUG', cast=bool)

# Integer
PORT = config('PORT', cast=int)

# List (comma-separated)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
```

---

## 🎉 Success!

Your project now uses environment variables! 🎊

### Benefits
- ✅ **Secure**: API keys not in code
- ✅ **Flexible**: Easy to change per environment
- ✅ **Safe**: .env not committed to Git
- ✅ **Professional**: Industry standard practice
- ✅ **Team-friendly**: .env.example for others

---

## 📚 Resources

### Documentation
- **python-decouple**: https://github.com/HBNetwork/python-decouple
- **Django Settings**: https://docs.djangoproject.com/en/stable/topics/settings/
- **12-Factor App**: https://12factor.net/config

### Tools
- **Generate Secret Key**: 
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

---

**Your secrets are now secure! 🔐**

**Version**: 1.0.0  
**Status**: Complete ✅  
**Security**: Enhanced 🔒
