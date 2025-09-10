#!/usr/bin/env python
"""
Simple import test
"""

print("Testing imports...")

try:
    import google
    print("✅ google package imported successfully")
    print(f"google package location: {google.__file__}")
except ImportError as e:
    print(f"❌ Failed to import google: {e}")

try:
    import google.genai
    print("✅ google.genai imported successfully")
except ImportError as e:
    print(f"❌ Failed to import google.genai: {e}")

try:
    from google import genai
    print("✅ from google import genai successful")
except ImportError as e:
    print(f"❌ Failed to import genai from google: {e}")

print("Import test complete.")