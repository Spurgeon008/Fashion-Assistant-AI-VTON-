# VTON Troubleshooting Guide

## Changes Made

### 1. Custom Prompt Support (Option 2)
You can now customize the VTON prompt by editing `greatkart/settings.py`:

```python
VTON_DEFAULT_PROMPT = "Combine the subjects of these images in a natural way, producing a new image."
```

Change this to any prompt you want, such as:
- `"Create a realistic virtual try-on showing the person wearing the clothing item"`
- `"Generate a professional fashion photo of the person wearing the garment"`
- `"Show the person wearing the clothes naturally with proper fit and lighting"`

**No code changes needed** - just edit the setting and restart Django!

### 2. Enhanced Error Handling
Added better error messages and validation:
- Image size validation (max 10MB per image)
- Automatic image resizing (max 2048px dimension)
- Better error messages for common API issues
- Detailed logging for debugging

### 3. Image Optimization
- Automatically resizes large images to prevent API errors
- Preserves original file extensions
- Optimizes image quality for faster processing

## Common Issues & Solutions

### Issue: "500 INTERNAL" Error from Gemini API

This error can occur for several reasons:

#### 1. Image Content Issues
The Gemini API may reject images with:
- Inappropriate content
- Very low quality or corrupted images
- Images that are too abstract or unclear

**Solution:** Try with different, clear images of people and clothing items.

#### 2. Image Size/Resolution Issues
Very large or high-resolution images can cause problems.

**Solution:** The code now automatically resizes images, but you can also:
- Use images under 2048x2048 pixels
- Keep file sizes under 5MB

#### 3. API Quota/Rate Limits
You may have exceeded your API quota.

**Solution:**
- Check your quota at: https://aistudio.google.com/app/apikey
- Wait a few minutes and try again
- Consider upgrading your API plan

#### 4. Temporary API Issues
Sometimes the Gemini API has temporary outages.

**Solution:** Wait a few minutes and try again.

### Issue: Images Not Uploading

**Check:**
1. File input accepts images: `accept="image/*"`
2. Form has `enctype="multipart/form-data"`
3. Both person and cloth images are selected

### Issue: Slow Response

**Normal behavior:**
- VTON generation typically takes 10-30 seconds
- The API processes images and generates new ones
- Be patient and don't refresh the page

## Testing Your Setup

### Test 1: API Connection
Run the basic API test:
```bash
python test_api_direct.py
```

### Test 2: Image Generation
Run the image generation test:
```bash
python test_vton_with_images.py
```

This will:
- Test with sample images from the nano-banana project
- Generate a test output image
- Verify your API key and setup work correctly

### Test 3: Django Integration
1. Start Django: `python manage.py runserver`
2. Go to a product detail page
3. Scroll to "Virtual Try-On" section
4. Upload clear images of a person and clothing
5. Click "Generate Try-On"

## Debugging Tips

### Check Django Logs
Look for DEBUG messages in your Django console:
```
DEBUG: Person image: photo.jpg, size: 123456 bytes
DEBUG: Cloth image: shirt.jpg, size: 234567 bytes
DEBUG: Generating VTON with images: [...]
DEBUG: Using prompt: Combine the subjects...
DEBUG: Generated 1 images
```

### Check Browser Console
Open browser DevTools (F12) and check:
- Network tab for API request/response
- Console tab for JavaScript errors

### Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "API key not set" | Missing API key | Add key to settings.py |
| "Both images required" | Missing upload | Select both images |
| "Image too large" | File > 10MB | Use smaller images |
| "500 INTERNAL" | API rejected request | Try different images |
| "quota exceeded" | API limit reached | Wait or upgrade plan |

## Best Practices

### For Best Results:
1. **Use clear, well-lit photos** of people
2. **Use clear product images** of clothing items
3. **Keep images under 5MB** each
4. **Use common formats** (JPG, PNG)
5. **Avoid extreme resolutions** (very small or very large)

### Recommended Image Specs:
- **Format:** JPG or PNG
- **Size:** 500KB - 5MB
- **Resolution:** 512x512 to 2048x2048 pixels
- **Content:** Clear, well-lit, single subject

## API Key Management

Your API key is in `greatkart/settings.py`:
```python
GEMINI_API_KEY = 'AIzaSy...'
```

**Security Tips:**
- Never commit API keys to Git
- Add `settings.py` to `.gitignore` if sharing code
- Use environment variables in production
- Rotate keys if exposed

## Need More Help?

1. Check the test scripts output for detailed errors
2. Review Django console logs
3. Check browser console for frontend errors
4. Verify API key at: https://aistudio.google.com/app/apikey
5. Check Gemini API status: https://status.cloud.google.com/

## Summary

The VTON system is now:
- ✅ Using customizable prompts from settings
- ✅ Automatically resizing large images
- ✅ Providing better error messages
- ✅ Validating image sizes
- ✅ Logging detailed debug information

Try uploading different images if you get 500 errors - the API can be sensitive to image content and quality.
