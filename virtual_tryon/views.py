import os
import mimetypes
import time
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import tempfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Test import at module level to catch issues early
try:
    from google import genai
    from google.genai import types
    GOOGLE_GENAI_IMPORT_SUCCESS = True
except ImportError as e:
    GOOGLE_GENAI_IMPORT_SUCCESS = False
    GOOGLE_GENAI_IMPORT_ERROR = str(e)

def _get_mime_type(file_path):
    """Guesses the MIME type of a file based on its extension."""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        raise ValueError(f"Could not determine MIME type for {file_path}")
    return mime_type

def _load_image_parts(image_paths):
    """Loads image files and converts them into GenAI Part objects."""
    # This will only be called if imports are successful
    parts = []
    for image_path in image_paths:
        with open(image_path, "rb") as f:
            image_data = f.read()
        mime_type = _get_mime_type(image_path)
        parts.append(
            types.Part(inline_data=types.Blob(data=image_data, mime_type=mime_type))
        )
    return parts

def remix_images(image_paths, prompt):
    """
    Remixes images using the Google Generative AI model.
    Exactly matches the working nano-banana implementation.

    Args:
        image_paths: A list of paths to input images.
        prompt: The prompt for remixing the images.

    Returns:
        List of generated images data
    """
    # Get API key from settings
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in Django settings")
    
    client = genai.Client(api_key=api_key)
    
    # Use exact model name from working implementation
    MODEL_NAME = "gemini-2.5-flash-image-preview"
    
    contents = _load_image_parts(image_paths)
    contents.append(genai.types.Part.from_text(text=prompt))
    
    generate_content_config = types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
    )
    
    # Use exact streaming approach from working implementation
    stream = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=contents,
        config=generate_content_config,
    )
    
    # Process stream exactly like working implementation
    images_data = []
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
    
    return images_data

@csrf_exempt
def generate_vton(request):
    """
    Handles the VTON image generation request.
    Expects POST request with 'person_image' and 'cloth_image' files.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    # Check if Google Generative AI library is available
    if not GOOGLE_GENAI_IMPORT_SUCCESS:
        return JsonResponse({'error': f'Google Generative AI library is not installed: {GOOGLE_GENAI_IMPORT_ERROR}'}, status=500)
    
    # Check API key
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key or not api_key.strip():
        return JsonResponse({'error': 'GEMINI_API_KEY is not set in Django settings. Please add your API key to settings.py'}, status=500)
    
    try:
        # Get the uploaded files
        person_image = request.FILES.get('person_image')
        cloth_image = request.FILES.get('cloth_image')
        
        if not person_image or not cloth_image:
            return JsonResponse({'error': 'Both person_image and cloth_image are required'}, status=400)
        
        # Create temporary files for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as person_temp:
            person_temp.write(person_image.read())
            person_temp_path = person_temp.name
            
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as cloth_temp:
            cloth_temp.write(cloth_image.read())
            cloth_temp_path = cloth_temp.name
        
        # Use the exact prompt from working implementation
        prompt = "Combine the subjects of these images in a natural way, producing a new image."
        
        # Generate the VTON image
        image_paths = [person_temp_path, cloth_temp_path]
        print(f"DEBUG: Generating VTON with images: {image_paths}")
        print(f"DEBUG: Using prompt: {prompt}")
        
        generated_images = remix_images(image_paths, prompt)
        
        # Clean up temporary files
        os.unlink(person_temp_path)
        os.unlink(cloth_temp_path)
        
        print(f"DEBUG: Generated {len(generated_images)} images")
        
        if not generated_images:
            return JsonResponse({'error': 'Failed to generate VTON image - no images returned'}, status=500)
        
        # For now, we'll return the first generated image
        generated_image_data = generated_images[0]
        
        # Return the image data as base64 for the frontend to display
        import base64
        image_base64 = base64.b64encode(generated_image_data).decode('utf-8')
        
        print(f"DEBUG: Returning image data (length: {len(image_base64)})")
        
        return JsonResponse({
            'success': True,
            'image_data': image_base64
        })
        
    except Exception as e:
        # Clean up temporary files if they exist
        try:
            os.unlink(person_temp_path)
        except:
            pass
        try:
            os.unlink(cloth_temp_path)
        except:
            pass
            
        # Return more detailed error information for debugging
        return JsonResponse({'error': f'VTON generation failed: {str(e)}'}, status=500)
