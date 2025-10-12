#!/usr/bin/env python
"""
Test VTON with actual images to diagnose the 500 INTERNAL error
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greatkart.settings')
django.setup()

from django.conf import settings

def test_with_sample_images():
    """Test with the sample images from nano-banana"""
    
    # Check API key
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key or not api_key.strip():
        print("❌ API key not set in settings.py")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        from google import genai
        from google.genai import types
        import mimetypes
        print("✅ Imports successful")
        
        # Use the sample images from nano-banana
        image1_path = "VTON/nano-banana-python-main/images/man.jpeg"
        image2_path = "VTON/nano-banana-python-main/images/yellow_jacket.jpeg"
        
        # Check if files exist
        if not os.path.exists(image1_path):
            print(f"❌ Image not found: {image1_path}")
            return False
        if not os.path.exists(image2_path):
            print(f"❌ Image not found: {image2_path}")
            return False
        
        print(f"✅ Found images: {image1_path}, {image2_path}")
        
        # Initialize client
        client = genai.Client(api_key=api_key)
        print("✅ Client initialized")
        
        # Load images
        def load_image_parts(image_paths):
            parts = []
            for image_path in image_paths:
                with open(image_path, "rb") as f:
                    image_data = f.read()
                mime_type, _ = mimetypes.guess_type(image_path)
                if mime_type is None:
                    mime_type = "image/jpeg"
                print(f"  - Loaded {image_path}: {len(image_data)} bytes, MIME: {mime_type}")
                parts.append(
                    types.Part(inline_data=types.Blob(data=image_data, mime_type=mime_type))
                )
            return parts
        
        contents = load_image_parts([image1_path, image2_path])
        
        # Add prompt
        prompt = "Combine the subjects of these images in a natural way, producing a new image."
        contents.append(genai.types.Part.from_text(text=prompt))
        print(f"✅ Prompt: {prompt}")
        
        # Configure generation
        MODEL_NAME = "gemini-2.5-flash-image-preview"
        generate_content_config = types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        )
        
        print(f"🔄 Calling API with model: {MODEL_NAME}")
        print("   This may take 10-30 seconds...")
        
        # Call API
        stream = client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=contents,
            config=generate_content_config,
        )
        
        # Process response
        images_data = []
        text_responses = []
        
        for chunk in stream:
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue

            for part in chunk.candidates[0].content.parts:
                if part.inline_data and part.inline_data.data:
                    images_data.append(part.inline_data.data)
                    print(f"✅ Received image: {len(part.inline_data.data)} bytes")
                elif part.text:
                    text_responses.append(part.text)
                    print(f"✅ Received text: {part.text[:100]}")
        
        if images_data:
            print(f"\n🎉 SUCCESS! Generated {len(images_data)} image(s)")
            
            # Save the first image for verification
            import base64
            output_path = "test_vton_output.jpg"
            with open(output_path, "wb") as f:
                f.write(images_data[0])
            print(f"✅ Saved test image to: {output_path}")
            return True
        else:
            print(f"\n⚠️  No images generated. Text responses: {text_responses}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== VTON Image Test ===\n")
    success = test_with_sample_images()
    if success:
        print("\n✅ Test passed! Your VTON should work.")
    else:
        print("\n❌ Test failed. Check the errors above.")
