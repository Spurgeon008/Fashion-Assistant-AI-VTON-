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
from PIL import Image
import io

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

def _resize_image_if_needed(image_path, max_dimension=2048):
    """Resize image if it's too large, to avoid API issues"""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            
            # Check if resizing is needed
            if width <= max_dimension and height <= max_dimension:
                return  # No resize needed
            
            # Calculate new dimensions maintaining aspect ratio
            if width > height:
                new_width = max_dimension
                new_height = int(height * (max_dimension / width))
            else:
                new_height = max_dimension
                new_width = int(width * (max_dimension / height))
            
            # Resize and save
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img_resized.save(image_path, quality=85, optimize=True)
            print(f"DEBUG: Resized image from {width}x{height} to {new_width}x{new_height}")
    except Exception as e:
        print(f"WARNING: Could not resize image: {e}")

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
def generate_video_vton(request):
    """
    Handles the VTON video generation request by triggering the n8n workflow.
    Expects POST request with 'person_image' file and 'prompt'.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        import requests
        import base64
        
        # Get the uploaded file and prompt
        person_image = request.FILES.get('person_image')
        cloth_image = request.FILES.get('cloth_image')
        prompt = request.POST.get('prompt', 'Create a video showing the person wearing this clothing item')
        user_id = request.POST.get('userid', request.user.id if request.user.is_authenticated else 'anonymous')
        
        if not person_image or not cloth_image:
            return JsonResponse({'error': 'Both person_image and cloth_image are required'}, status=400)
        
        # Read and encode images to base64
        person_image_data = person_image.read()
        cloth_image_data = cloth_image.read()
        
        person_base64 = base64.b64encode(person_image_data).decode('utf-8')
        cloth_base64 = base64.b64encode(cloth_image_data).decode('utf-8')
        
        # Get n8n webhook URL from settings
        n8n_webhook_url = getattr(settings, 'N8N_VIDEO_WEBHOOK_URL', 'http://localhost:5678/webhook/video-vton')
        
        # Prepare the payload matching the video.json workflow structure
        payload = {
            'body': {
                'prompt': prompt,
                'userid': user_id,
                'output': '2-image'  # This triggers the video generation path
            },
            'binary': {
                'image0': {
                    'data': person_base64,
                    'mimeType': person_image.content_type or 'image/jpeg'
                },
                'image1': {
                    'data': cloth_base64,
                    'mimeType': cloth_image.content_type or 'image/jpeg'
                }
            }
        }
        
        print(f"DEBUG: Triggering n8n video workflow at {n8n_webhook_url}")
        print(f"DEBUG: Prompt: {prompt}")
        print(f"DEBUG: User ID: {user_id}")
        
        # Trigger the n8n workflow
        response = requests.post(
            n8n_webhook_url,
            json=payload,
            timeout=300  # 5 minute timeout for video generation
        )
        
        if response.status_code == 200:
            result = response.json()
            return JsonResponse({
                'success': True,
                'message': 'Video generation started successfully',
                'workflow_response': result
            })
        else:
            return JsonResponse({
                'error': f'n8n workflow failed with status {response.status_code}',
                'details': response.text
            }, status=500)
            
    except requests.exceptions.Timeout:
        return JsonResponse({
            'error': 'Video generation timed out. The process may still be running in the background.'
        }, status=504)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR: Video VTON generation failed")
        print(error_details)
        
        return JsonResponse({
            'error': f'Video VTON generation failed: {str(e)}'
        }, status=500)

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
        
        # Validate image sizes (max 10MB each)
        MAX_SIZE = 10 * 1024 * 1024  # 10MB
        if person_image.size > MAX_SIZE:
            return JsonResponse({'error': f'Person image too large. Max size: 10MB, got: {person_image.size / 1024 / 1024:.1f}MB'}, status=400)
        if cloth_image.size > MAX_SIZE:
            return JsonResponse({'error': f'Cloth image too large. Max size: 10MB, got: {cloth_image.size / 1024 / 1024:.1f}MB'}, status=400)
        
        print(f"DEBUG: Person image: {person_image.name}, size: {person_image.size} bytes")
        print(f"DEBUG: Cloth image: {cloth_image.name}, size: {cloth_image.size} bytes")
        
        # Create temporary files for processing
        # Use the original file extension if possible
        person_ext = os.path.splitext(person_image.name)[1] or '.jpg'
        cloth_ext = os.path.splitext(cloth_image.name)[1] or '.jpg'
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=person_ext) as person_temp:
            person_temp.write(person_image.read())
            person_temp_path = person_temp.name
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=cloth_ext) as cloth_temp:
            cloth_temp.write(cloth_image.read())
            cloth_temp_path = cloth_temp.name
        
        # Resize images if they're too large
        _resize_image_if_needed(person_temp_path)
        _resize_image_if_needed(cloth_temp_path)
        
        # Use prompt from settings (can be customized in settings.py)
        prompt = getattr(settings, 'VTON_DEFAULT_PROMPT', "Combine the subjects of these images in a natural way, producing a new image.")
        
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
        
        # Log the full error for debugging
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR: VTON generation failed")
        print(error_details)
        
        # Return more detailed error information for debugging
        error_message = str(e)
        
        # Check for common API errors
        if "500 INTERNAL" in error_message:
            error_message = "Gemini API returned an internal error. This could be due to: image content, size, or temporary API issues. Try with different images or try again later."
        elif "quota" in error_message.lower():
            error_message = "API quota exceeded. Check your Gemini API usage limits."
        elif "invalid" in error_message.lower() and "key" in error_message.lower():
            error_message = "Invalid API key. Please check your GEMINI_API_KEY in settings.py"
        
        return JsonResponse({'error': f'VTON generation failed: {error_message}'}, status=500)
