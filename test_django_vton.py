#!/usr/bin/env python
"""
Test Django VTON integration to diagnose issues after environment variable abstraction
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greatkart.settings')
django.setup()

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from virtual_tryon.views import generate_vton

def test_django_vton_view():
    """Test the Django VTON view with sample images"""
    
    print("=== Testing Django VTON Integration ===\n")
    
    # Step 1: Check settings
    print("1. Checking Django Settings...")
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key or not api_key.strip():
        print("   ❌ GEMINI_API_KEY not set in Django settings")
        return False
    print(f"   ✅ API Key: {api_key[:20]}...")
    
    # Step 2: Check imports
    print("\n2. Checking imports...")
    try:
        from google import genai
        from google.genai import types
        print("   ✅ Google Generative AI imports successful")
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    
    # Step 3: Load test images
    print("\n3. Loading test images...")
    image1_path = "VTON/nano-banana-python-main/images/man.jpeg"
    image2_path = "VTON/nano-banana-python-main/images/yellow_jacket.jpeg"
    
    if not os.path.exists(image1_path) or not os.path.exists(image2_path):
        print(f"   ❌ Test images not found")
        return False
    
    with open(image1_path, 'rb') as f:
        person_image_data = f.read()
    with open(image2_path, 'rb') as f:
        cloth_image_data = f.read()
    
    print(f"   ✅ Person image: {len(person_image_data)} bytes")
    print(f"   ✅ Cloth image: {len(cloth_image_data)} bytes")
    
    # Step 4: Create mock request
    print("\n4. Creating mock Django request...")
    factory = RequestFactory()
    
    person_file = SimpleUploadedFile(
        "person.jpg",
        person_image_data,
        content_type="image/jpeg"
    )
    cloth_file = SimpleUploadedFile(
        "cloth.jpg",
        cloth_image_data,
        content_type="image/jpeg"
    )
    
    request = factory.post(
        '/vton/generate/',
        {
            'person_image': person_file,
            'cloth_image': cloth_file
        }
    )
    print("   ✅ Mock request created")
    
    # Step 5: Call the view
    print("\n5. Calling generate_vton view...")
    print("   ⏳ This may take 10-30 seconds...")
    
    try:
        response = generate_vton(request)
        
        if response.status_code == 200:
            import json
            data = json.loads(response.content)
            
            if data.get('success'):
                print(f"   ✅ SUCCESS! Generated image")
                print(f"   ✅ Image data length: {len(data.get('image_data', ''))} chars")
                
                # Save the image for verification
                import base64
                image_data = base64.b64decode(data['image_data'])
                output_path = "test_django_vton_output.jpg"
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                print(f"   ✅ Saved output to: {output_path}")
                return True
            else:
                print(f"   ❌ Response not successful: {data}")
                return False
        else:
            print(f"   ❌ HTTP {response.status_code}: {response.content.decode()}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error calling view: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_django_vton_view()
    
    if success:
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("="*50)
        print("\nYour Django VTON integration is working correctly.")
        print("If you're still experiencing issues in the browser:")
        print("1. Check browser console for JavaScript errors")
        print("2. Verify the form has enctype='multipart/form-data'")
        print("3. Check Django server logs for errors")
    else:
        print("\n" + "="*50)
        print("❌ TESTS FAILED")
        print("="*50)
        print("\nCheck the errors above to diagnose the issue.")
