#!/usr/bin/env python
"""
Direct API test using the exact working implementation
"""

import os
import sys
import django
import tempfile
import mimetypes

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greatkart.settings')
django.setup()

from django.conf import settings

def test_direct_api():
    """Test the API directly using the exact working code structure"""
    
    # Check API key
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key or not api_key.strip():
        print("❌ API key not set in settings.py")
        return False
    
    try:
        # Import exactly like working code
        from google import genai
        from google.genai import types
        print("✅ Imports successful")
        
        # Initialize client exactly like working code
        client = genai.Client(api_key=api_key)
        print("✅ Client initialized")
        
        # Test with a simple text-only request first
        MODEL_NAME = "gemini-2.5-flash-image-preview"
        
        # Create a simple text content
        contents = [genai.types.Part.from_text(text="Hello, can you respond with a simple greeting?")]
        
        generate_content_config = types.GenerateContentConfig(
            response_modalities=["TEXT"],  # Text only for initial test
        )
        
        print("🔄 Testing API connection...")
        
        # Test streaming response
        stream = client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=contents,
            config=generate_content_config,
        )
        
        response_received = False
        for chunk in stream:
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue

            for part in chunk.candidates[0].content.parts:
                if part.text:
                    print(f"✅ API Response: {part.text[:100]}...")
                    response_received = True
                    break
            
            if response_received:
                break
        
        if response_received:
            print("✅ API is working correctly!")
            return True
        else:
            print("❌ No response received from API")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Direct API Test ===")
    success = test_direct_api()
    if success:
        print("\n🎉 Your setup is working! The VTON should work now.")
        print("Make sure to:")
        print("1. Add your actual API key to settings.py")
        print("2. Test the VTON functionality in your Django app")
    else:
        print("\n❌ Setup needs fixing. Check the errors above.")