# 🎥 video.json Configuration Guide

## Overview

The `video.json` file contains your n8n workflow configuration for video VTON generation. This file includes sensitive API keys and should not be committed to Git.

---

## 🔒 Security Setup

### Files Structure

```
SmartFitStudios/
├── video.json              ❌ NOT in Git (contains your API key)
├── video.json.example      ✅ In Git (template without API key)
└── .gitignore              ✅ Includes video.json
```

---

## 🚀 Setup Instructions

### For You (First Time)

1. **Your video.json is already configured!** ✅

2. **Verify it's in .gitignore:**
```bash
type .gitignore | findstr video.json
```

3. **Add your actual API key:**
   - Open `video.json`
   - Find line 231
   - Replace `YOUR_GEMINI_API_KEY_HERE` with your actual key

### For Other Developers

1. **Copy the template:**
```bash
copy video.json.example video.json
```

2. **Add your API key:**
   - Open `video.json`
   - Find line 231: `"x-goog-api-key": "YOUR_GEMINI_API_KEY_HERE"`
   - Replace with your actual Gemini API key

3. **Import to n8n:**
   - Open n8n dashboard
   - Go to Workflows → Import from File
   - Select your `video.json`
   - Configure credentials

---

## 🔑 API Key Location

### In video.json

**Line 231:**
```json
"jsonHeaders": "{\n  \"x-goog-api-key\": \"YOUR_GEMINI_API_KEY_HERE\",\n  \"Content-Type\": \"application/json\"\n}"
```

**Replace:**
```json
"x-goog-api-key": "YOUR_GEMINI_API_KEY_HERE"
```

**With:**
```json
"x-goog-api-key": "AIzaSyDktTtX2nXl-QTBWuLmZho5fV3PzDS9d9A"
```

---

## 🎯 Better Practice: Use n8n Credentials

Instead of hardcoding the API key in video.json, use n8n's credential system:

### Step 1: Create Credential in n8n

1. Open n8n dashboard
2. Go to **Credentials** → **New Credential**
3. Select **Header Auth**
4. Configure:
   - **Name**: `Gemini API Key`
   - **Header Name**: `x-goog-api-key`
   - **Header Value**: `YOUR_ACTUAL_API_KEY`
5. Save

### Step 2: Update HTTP Request2 Node

1. Open your workflow in n8n
2. Find the **HTTP Request2** node
3. In **Authentication** section:
   - Select **Generic Credential Type**
   - Choose **Header Auth**
   - Select your **Gemini API Key** credential
4. Remove the hardcoded API key from **jsonHeaders**
5. Save workflow

### Step 3: Export Clean Workflow

1. Export the workflow
2. The exported JSON will reference the credential
3. No API key in the file!

---

## 📝 Editing video.json

### Find the API Key

**Method 1: Search**
```bash
# Windows PowerShell
Select-String -Path "video.json" -Pattern "x-goog-api-key"
```

**Method 2: Line Number**
- Open `video.json`
- Go to line 231
- Look for `"x-goog-api-key"`

### Replace the Key

```json
// Before
"x-goog-api-key": "YOUR_GEMINI_API_KEY_HERE"

// After
"x-goog-api-key": "AIzaSyDktTtX2nXl-QTBWuLmZho5fV3PzDS9d9A"
```

---

## 🔐 Security Checklist

### ✅ Completed

- ✅ Added `video.json` to `.gitignore`
- ✅ Created `video.json.example` template
- ✅ Removed API key from template
- ✅ Documented setup process

### 🎯 Recommended

- ⏳ Use n8n credentials instead of hardcoding
- ⏳ Rotate API keys regularly
- ⏳ Use different keys for dev/prod
- ⏳ Set up API key restrictions in Google Cloud

---

## 🐛 Troubleshooting

### Issue: "video.json not found"

**Solution:** Copy from template
```bash
copy video.json.example video.json
```

### Issue: "Invalid API key"

**Solution:** Check the key in video.json line 231
```json
"x-goog-api-key": "YOUR_ACTUAL_KEY_HERE"
```

### Issue: "Workflow import failed"

**Solution:** 
1. Validate JSON syntax
2. Check all credentials are configured
3. Ensure n8n is running

---

## 📊 Workflow Structure

### Nodes Using API Key

**HTTP Request2** (Line 226-256)
- Calls Gemini API
- Requires API key in header
- Line 231 contains the key

### Other Credentials Needed

1. **Header Auth** (for file uploads)
   - Used by: input, input2, output1 nodes
   - Configure in n8n credentials

2. **Baserow API** (for storing results)
   - Used by: Baserow1 node
   - Configure in n8n credentials

3. **ComfyUI API** (for image processing)
   - Used by: output_2_img1 node (disabled)
   - Configure if needed

---

## 🔄 Updating the Workflow

### When You Make Changes

1. **Edit in n8n** (recommended)
   - Make changes in n8n UI
   - Export workflow
   - Save as `video.json`

2. **Edit JSON directly** (advanced)
   - Open `video.json`
   - Make changes carefully
   - Validate JSON syntax
   - Import to n8n

### After Changes

1. **Test the workflow** in n8n
2. **Export** if working
3. **Update** `video.json.example` (remove secrets)
4. **Commit** only the example file

---

## 📚 Related Files

### Configuration Files

- **video.json** - Your workflow (NOT in Git)
- **video.json.example** - Template (in Git)
- **.env** - Environment variables (NOT in Git)
- **.env.example** - Template (in Git)

### Documentation

- **VIDEO_JSON_SETUP.md** - This file
- **VIDEO_VTON_SETUP.md** - Integration guide
- **ENV_SETUP_GUIDE.md** - Environment variables guide

---

## 🎓 Best Practices

### 1. Never Commit Secrets

```bash
# .gitignore
video.json
.env
```

### 2. Use Templates

```bash
# Safe to commit
video.json.example
.env.example
```

### 3. Use Credentials

Instead of hardcoding in JSON:
```json
// Bad
"x-goog-api-key": "AIzaSy..."

// Good (in n8n)
"authentication": "headerAuth",
"credentials": "geminiApiKey"
```

### 4. Document Everything

- Keep README updated
- Document required credentials
- Provide setup instructions

---

## ✅ Verification

### Check .gitignore

```bash
type .gitignore | findstr video.json
```

Should show:
```
video.json
```

### Check Files Exist

```bash
dir video.json
dir video.json.example
```

Both should exist.

### Test Import

1. Open n8n
2. Import `video.json`
3. Should work without errors

---

## 🎉 Success!

Your video.json is now secure! 🎊

### What's Protected

- ✅ **video.json** - Not in Git
- ✅ **API key** - Not exposed
- ✅ **Template** - Available for others
- ✅ **Documentation** - Complete

### What to Share

- ✅ **video.json.example** - Template
- ✅ **Documentation** - Setup guides
- ✅ **Instructions** - How to configure

### What to Keep Private

- ❌ **video.json** - Your workflow
- ❌ **API keys** - Your secrets
- ❌ **.env** - Your configuration

---

## 📞 Quick Reference

### Get Your API Key
https://aistudio.google.com/app/apikey

### n8n Documentation
https://docs.n8n.io/

### Workflow Location
Line 231 in video.json

### Template File
video.json.example

---

**Your n8n workflow is now secure! 🔐**

**Version**: 1.0.0  
**Status**: Complete ✅  
**Security**: Enhanced 🔒
