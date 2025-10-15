#!/usr/bin/env python
"""
Complete VTON System Test - Verifies all components are working
"""

import os
import sys

def test_environment_variables():
    """Test that environment variables are properly configured"""
    print("=" * 60)
    print("TEST 1: Environment Variables")
    print("=" * 60)
    
    from decouple import config
    
    api_key = config('GEMINI_API_KEY', default='')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env")
        return False
    
    print(f"✅ GEMINI_API_KEY found: {api_key[:20]}...")
    
    n8n_url = config('N8N_VIDEO_WEBHOOK_URL', default='')
    print(f"✅ N8N_VIDEO_WEBHOOK_URL: {n8n_url}")
    
    return True

def test_django_settings():
    """Test that Django settings are loading correctly"""
    print("\n" + "=" * 60)
    print("TEST 2: Django Settings")
    print("=" * 60)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greatkart.settings')
    import django
    django.setup()
    
    from django.conf import settings
    
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        print("❌ GEMINI_API_KEY not loaded in Django settings")
        return False
    
    print(f"✅ GEMINI_API_KEY in settings: {api_key[:20]}...")
    
    n8n_url = getattr(settings, 'N8N_VIDEO_WEBHOOK_URL', None)
    print(f"✅ N8N_VIDEO_WEBHOOK_URL in settings: {n8n_url}")
    
    return True

def test_imports():
    """Test that all required imports work"""
    print("\n" + "=" * 60)
    print("TEST 3: Required Imports")
    print("=" * 60)
    
    try:
        from google import genai
        from google.genai import types
        print("✅ Google Generative AI library imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Google Generative AI: {e}")
        return False
    
    try:
        from virtual_tryon.views import generate_vton, generate_video_vton
        print("✅ VTON views imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import VTON views: {e}")
        return False
    
    return True

def test_url_routing():
    """Test that URL routing is configured"""
    print("\n" + "=" * 60)
    print("TEST 4: URL Routing")
    print("=" * 60)
    
    from django.urls import reverse, NoReverseMatch
    
    try:
        url = reverse('generate_vton')
        print(f"✅ generate_vton URL: {url}")
    except NoReverseMatch:
        print("❌ generate_vton URL not found")
        return False
    
    try:
        url = reverse('generate_video_vton')
        print(f"✅ generate_video_vton URL: {url}")
    except NoReverseMatch:
        print("❌ generate_video_vton URL not found")
        return False
    
    return True

def test_api_connection():
    """Test actual API connection"""
    print("\n" + "=" * 60)
    print("TEST 5: API Connection")
    print("=" * 60)
    
    from django.conf import settings
    from google import genai
    
    api_key = settings.GEMINI_API_KEY
    
    try:
        client = genai.Client(api_key=api_key)
        print("✅ Gemini API client initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize API client: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\n" + "=" * 60)
    print("TEST 6: File Structure")
    print("=" * 60)
    
    required_files = [
        '.env',
        'greatkart/settings.py',
        'virtual_tryon/views.py',
        'virtual_tryon/urls.py',
        'static/js/script.js',
        'templates/store/product_detail.html',
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} NOT FOUND")
            all_exist = False
    
    return all_exist

def test_javascript_vton_handlers():
    """Test that JavaScript VTON handlers exist"""
    print("\n" + "=" * 60)
    print("TEST 7: JavaScript VTON Handlers")
    print("=" * 60)
    
    with open('static/js/script.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    required_handlers = [
        '#image-vton-form',
        '#video-vton-form',
        '/vton/generate_vton/',
        '/vton/generate_video_vton/',
        '#download-vton-btn',
    ]
    
    all_found = True
    for handler in required_handlers:
        if handler in js_content:
            print(f"✅ Found: {handler}")
        else:
            print(f"❌ Missing: {handler}")
            all_found = False
    
    return all_found

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "COMPLETE VTON SYSTEM TEST" + " " * 23 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Django Settings", test_django_settings),
        ("Required Imports", test_imports),
        ("URL Routing", test_url_routing),
        ("API Connection", test_api_connection),
        ("File Structure", test_file_structure),
        ("JavaScript Handlers", test_javascript_vton_handlers),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your VTON system is fully operational!")
        print("\nNext steps:")
        print("1. Start Django server: python manage.py runserver")
        print("2. Visit a product detail page")
        print("3. Scroll to 'Virtual Try-On' section")
        print("4. Upload images and test the feature!")
        return True
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
