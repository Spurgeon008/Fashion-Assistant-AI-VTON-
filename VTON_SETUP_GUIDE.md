# VTON Setup Guide

## Quick Fix Steps

### 1. Add Your API Key
Open `greatkart/settings.py` and replace the empty string with your actual Gemini API key:

```python
# Replace this line:
GEMINI_API_KEY = ''

# With your actual key:
GEMINI_API_KEY = 'your_actual_gemini_api_key_here'
```

### 2. Test Your Setup
Run the test script to verify everything works:

```bash
python test_api_direct.py
```

### 3. Test VTON in Browser
1. Start your Django server: `python manage.py runserver`
2. Go to any product detail page
3. Scroll down to the "Virtual Try-On" section
4. Upload a person image and cloth image
5. Click "Generate Try-On (Image)"

## What Was Fixed

The main issues were:

1. **Import Statement**: Changed from `import google.genai as genai` to `from google import genai` to match the working implementation
2. **Model Name**: Using the exact model name `gemini-2.5-flash-image-preview` from the working code
3. **API Structure**: Matched the exact API call structure from the nano-banana implementation
4. **Response Processing**: Using the exact streaming response processing logic

## Troubleshooting

### If you get "API key not set" error:
- Make sure you've added your actual API key to `settings.py`
- The key should be a long string starting with something like `AIza...`

### If you get import errors:
- Make sure `google-genai` is installed: `pip install google-genai`
- Check that it's in your `requirements.txt`

### If the API call fails:
- Verify your API key is valid at https://aistudio.google.com/app/apikey
- Check that you have sufficient quota/credits
- Run `python test_api_direct.py` to test the connection

### If images don't display:
- Check the browser console for JavaScript errors
- Verify the AJAX request is reaching the Django endpoint
- Check Django logs for any server-side errors

## Files Modified

- `virtual_tryon/views.py` - Fixed API implementation
- `templates/base.html` - Improved JavaScript error handling
- `greatkart/settings.py` - Added API key placeholder
- Added test scripts for verification

The implementation now exactly matches the working nano-banana-python code structure.