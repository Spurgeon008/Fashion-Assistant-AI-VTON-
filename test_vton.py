#!/usr/bin/env python
"""
Test script for VTON functionality
Run this to test if your API key and setup work correctly
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greatkart.settings')
django.setup()

from django.conf import settings
from virtual_tryon.views import GOOGLE_GENAI_IMPORT_SUCCESS, GOOGLE_GENAI_IMPORT_ERROR

def test_vton_setup():
    print("=== VTON Setup Test ===")
    
    # Test 1: Check Google GenAI import
    print(f"1. Google GenAI Import: {'✓ SUCCESS' if GOOGLE_GENAI_IMPORT_SUCCESS else '✗ FAILED'}")
    if not GOOGLE_GENAI_IMPORT_SUCCESS:
        print(f"   Error: {GOOGLE_GENAI_IMPORT_ERROR}")
        return False
    
    # Test 2: Check API key
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key or not api_key.strip():
        print("2. API Key: ✗ NOT SET")
        print("   Please set GEMINI_API_KEY in your settings.py file")
        return False
    elif len(api_key.strip()) < 10:
        print("2. API Key: ✗ TOO SHORT")
        print("   API key seems too short, please check if it's correct")
        return False
    else:
        print("2. API Key: ✓ SET")
    
    # Test 3: Try to initialize client (using exact import from working code)
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        print("3. Client Initialization: ✓ SUCCESS")
    except Exception as e:
        print(f"3. Client Initialization: ✗ FAILED")
        print(f"   Error: {str(e)}")
        return False
    
    print("\n=== All tests passed! VTON should work correctly ===")
    return True

if __name__ == "__main__":
    test_vton_setup()