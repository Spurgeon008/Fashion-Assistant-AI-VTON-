from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import WardrobeItem, Outfit, WardrobeStats
from .forms import WardrobeItemForm, OutfitForm, ManualItemForm
from store.models import Product
import json
import random

# Try to import google.generativeai, use dummy if not available
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None

def wardrobe_dashboard(request):
    """Main wardrobe dashboard"""
    # Create a session-based wardrobe if user is not authenticated
    if request.user.is_authenticated:
        # Get or create user stats
        stats, created = WardrobeStats.objects.get_or_create(user=request.user)
        if created or request.GET.get('refresh_stats'):
            stats.update_stats()
        
        # Get recent items
        recent_items = WardrobeItem.objects.filter(user=request.user)[:8]
        
        # Get favorite items
        favorite_items = WardrobeItem.objects.filter(user=request.user, favorite=True)[:6]
        
        # Get recent outfits
        recent_outfits = Outfit.objects.filter(user=request.user)[:4]
        
        # Category breakdown
        category_stats = WardrobeItem.objects.filter(user=request.user).values('category').annotate(
            count=Count('id')
        ).order_by('-count')
    else:
        # For anonymous users, create empty data or use session data
        stats = None
        recent_items = []
        favorite_items = []
        recent_outfits = []
        category_stats = []
    
    context = {
        'stats': stats,
        'recent_items': recent_items,
        'favorite_items': favorite_items,
        'recent_outfits': recent_outfits,
        'category_stats': category_stats,
    }
    
    return render(request, 'wardrobe/dashboard.html', context)

def wardrobe_items(request):
    """View all wardrobe items with filtering"""
    if request.user.is_authenticated:
        items = WardrobeItem.objects.filter(user=request.user)
    else:
        items = WardrobeItem.objects.none()  # Empty queryset for anonymous users
    
    # Filtering
    category = request.GET.get('category')
    season = request.GET.get('season')
    source = request.GET.get('source')
    search = request.GET.get('search')
    
    if category:
        items = items.filter(category=category)
    if season:
        items = items.filter(season=season)
    if source:
        items = items.filter(source=source)
    if search:
        items = items.filter(
            Q(name__icontains=search) |
            Q(brand__icontains=search) |
            Q(color__icontains=search) |
            Q(tags__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    categories = WardrobeItem.CLOTHING_CATEGORIES
    seasons = WardrobeItem.SEASONS
    sources = WardrobeItem.SOURCE_CHOICES
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'seasons': seasons,
        'sources': sources,
        'current_filters': {
            'category': category,
            'season': season,
            'source': source,
            'search': search,
        }
    }
    
    return render(request, 'wardrobe/items.html', context)

def add_manual_item(request):
    """Add item manually to wardrobe"""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please sign in to add items to your wardrobe, or continue browsing as a guest.')
        return redirect('accounts:login')
    
    if request.method == 'POST':
        form = ManualItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.source = 'manual_upload'
            item.save()
            
            # Update stats
            stats, created = WardrobeStats.objects.get_or_create(user=request.user)
            stats.update_stats()
            
            messages.success(request, f'{item.name} has been added to your wardrobe!')
            return redirect('wardrobe:dashboard')
    else:
        form = ManualItemForm()
    
    return render(request, 'wardrobe/add_item.html', {'form': form})

def item_detail(request, item_id):
    """View item details"""
    if request.user.is_authenticated:
        item = get_object_or_404(WardrobeItem, id=item_id, user=request.user)
    else:
        # For anonymous users, redirect to login or show a message
        messages.warning(request, 'Please sign in to view item details.')
        return redirect('accounts:login')
    
    # Get outfits containing this item
    outfits = item.outfits.all()
    
    context = {
        'item': item,
        'outfits': outfits,
    }
    
    return render(request, 'wardrobe/item_detail.html', context)

def edit_item(request, item_id):
    """Edit wardrobe item"""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please sign in to edit items.')
        return redirect('accounts:login')
    
    item = get_object_or_404(WardrobeItem, id=item_id, user=request.user)
    
    if request.method == 'POST':
        form = WardrobeItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'{item.name} has been updated!')
            return redirect('wardrobe:item_detail', item_id=item.id)
    else:
        form = WardrobeItemForm(instance=item)
    
    return render(request, 'wardrobe/edit_item.html', {'form': form, 'item': item})

@require_POST
def delete_item(request, item_id):
    """Delete wardrobe item"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'})
    
    item = get_object_or_404(WardrobeItem, id=item_id, user=request.user)
    item_name = item.name
    item.delete()
    
    # Update stats
    stats, created = WardrobeStats.objects.get_or_create(user=request.user)
    stats.update_stats()
    
    messages.success(request, f'{item_name} has been removed from your wardrobe.')
    return redirect('wardrobe:items')

@require_POST
def toggle_favorite(request, item_id):
    """Toggle favorite status of an item"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'})
    
    item = get_object_or_404(WardrobeItem, id=item_id, user=request.user)
    item.favorite = not item.favorite
    item.save()
    
    return JsonResponse({
        'success': True,
        'favorite': item.favorite
    })

@require_POST
def mark_worn(request, item_id):
    """Mark item as worn today"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'})
    
    item = get_object_or_404(WardrobeItem, id=item_id, user=request.user)
    item.mark_as_worn()
    
    return JsonResponse({
        'success': True,
        'times_worn': item.times_worn,
        'last_worn': item.last_worn.strftime('%Y-%m-%d') if item.last_worn else None
    })

def outfits_list(request):
    """View all outfits"""
    if request.user.is_authenticated:
        outfits = Outfit.objects.filter(user=request.user)
    else:
        outfits = Outfit.objects.none()  # Empty queryset for anonymous users
    
    # Filtering
    season = request.GET.get('season')
    search = request.GET.get('search')
    
    if season:
        outfits = outfits.filter(season=season)
    if search:
        outfits = outfits.filter(
            Q(name__icontains=search) |
            Q(occasion__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(outfits, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'seasons': WardrobeItem.SEASONS,
        'current_filters': {
            'season': season,
            'search': search,
        }
    }
    
    return render(request, 'wardrobe/outfits.html', context)

def create_outfit(request):
    """Create new outfit"""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please sign in to create outfits.')
        return redirect('accounts:login')
    
    if request.method == 'POST':
        form = OutfitForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            outfit = form.save(commit=False)
            outfit.user = request.user
            outfit.save()
            form.save_m2m()  # Save many-to-many relationships
            
            # Update stats
            stats, created = WardrobeStats.objects.get_or_create(user=request.user)
            stats.update_stats()
            
            messages.success(request, f'Outfit "{outfit.name}" has been created!')
            return redirect('wardrobe:outfit_detail', outfit_id=outfit.id)
    else:
        form = OutfitForm(user=request.user)
    
    return render(request, 'wardrobe/create_outfit.html', {'form': form})

def outfit_detail(request, outfit_id):
    """View outfit details"""
    if request.user.is_authenticated:
        outfit = get_object_or_404(Outfit, id=outfit_id, user=request.user)
    else:
        messages.warning(request, 'Please sign in to view outfit details.')
        return redirect('accounts:login')
    
    context = {
        'outfit': outfit,
    }
    
    return render(request, 'wardrobe/outfit_detail.html', context)

def generate_outfit_ai(request):
    """AI-powered outfit generation based on user's wardrobe"""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please sign in to generate AI outfits from your wardrobe.')
        return redirect('accounts:login')
    
    user_items = WardrobeItem.objects.filter(user=request.user)
    
    if not user_items.exists():
        messages.error(request, 'You need to add some items to your wardrobe first!')
        return redirect('wardrobe:add_item')
    
    if request.method == 'POST':
        occasion = request.POST.get('occasion', 'casual')
        season = request.POST.get('season', 'all_season')
        style_preference = request.POST.get('style_preference', 'balanced')
        
        try:
            # Generate outfit suggestions using AI
            outfit_suggestions = generate_ai_outfit_suggestions(
                user_items, occasion, season, style_preference
            )
            
            context = {
                'outfit_suggestions': outfit_suggestions,
                'occasion': occasion,
                'season': season,
                'style_preference': style_preference,
                'user_items': user_items,
            }
            
            return render(request, 'wardrobe/ai_outfit_results.html', context)
            
        except Exception as e:
            messages.error(request, f'Error generating outfits: {str(e)}')
            return redirect('wardrobe:generate_outfit')
    
    # GET request - show the form
    context = {
        'seasons': WardrobeItem.SEASONS,
        'user_items_count': user_items.count(),
        'categories_available': user_items.values_list('category', flat=True).distinct(),
    }
    
    return render(request, 'wardrobe/generate_outfit.html', context)

def generate_ai_outfit_suggestions(user_items, occasion, season, style_preference):
    """
    Use AI to generate outfit suggestions based on user's wardrobe
    """
    # Check if AI is available and configured
    if not GENAI_AVAILABLE:
        return create_smart_outfit_suggestions(user_items, occasion, season, style_preference)
    
    # Get API key
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key or api_key == 'place_holder':
        return create_smart_outfit_suggestions(user_items, occasion, season, style_preference)
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Prepare wardrobe data for AI
        wardrobe_data = []
        for item in user_items:
            item_info = {
                'id': item.id,
                'name': item.name,
                'category': item.get_category_display(),
                'color': item.color or 'unspecified',
                'brand': item.brand or 'unspecified',
                'season': item.get_season_display(),
                'tags': item.get_tags_list(),
                'times_worn': item.times_worn,
            }
            wardrobe_data.append(item_info)
        
        # Create AI prompt
        prompt = f"""
        You are a professional fashion stylist. I need you to create 3 different outfit combinations from the following wardrobe items.

        WARDROBE ITEMS:
        {json.dumps(wardrobe_data, indent=2)}

        REQUIREMENTS:
        - Occasion: {occasion}
        - Season: {season}
        - Style preference: {style_preference}
        
        INSTRUCTIONS:
        1. Create 3 different complete outfits
        2. Each outfit should include items from different categories (tops, bottoms, shoes, etc.)
        3. Consider color coordination and style compatibility
        4. Prioritize items that haven't been worn much (low times_worn)
        5. Match the season and occasion requirements
        6. Provide a brief explanation for each outfit choice

        RESPONSE FORMAT (JSON):
        {{
            "outfits": [
                {{
                    "name": "Outfit Name",
                    "description": "Brief description of the outfit and why it works",
                    "items": [item_id1, item_id2, item_id3],
                    "style_notes": "Styling tips and why these items work together"
                }}
            ]
        }}

        Only return valid JSON, no additional text.
        """
        
        response = model.generate_content(prompt)
        
        # Parse AI response
        ai_response = response.text.strip()
        
        # Clean up the response if it has markdown formatting
        if ai_response.startswith('```json'):
            ai_response = ai_response.replace('```json', '').replace('```', '').strip()
        
        outfit_data = json.loads(ai_response)
        
        # Process the suggestions and add actual item objects
        processed_suggestions = []
        for outfit in outfit_data.get('outfits', []):
            # Get the actual item objects
            item_ids = outfit.get('items', [])
            outfit_items = user_items.filter(id__in=item_ids)
            
            if outfit_items.exists():  # Only include outfits with valid items
                processed_suggestions.append({
                    'name': outfit.get('name', 'AI Generated Outfit'),
                    'description': outfit.get('description', ''),
                    'style_notes': outfit.get('style_notes', ''),
                    'items': outfit_items,
                    'item_ids': item_ids,
                })
        
        return processed_suggestions
        
    except Exception as e:
        # Fallback: create smart combinations if AI fails
        return create_smart_outfit_suggestions(user_items, occasion, season, style_preference)

def create_smart_outfit_suggestions(user_items, occasion, season, style_preference):
    """
    Create smart outfit suggestions using rule-based logic (no AI required)
    """
    suggestions = []
    
    # Group items by category
    categories = {}
    for item in user_items:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)
    
    # Define outfit rules based on occasion
    outfit_rules = {
        'casual': {
            'required': ['tops', 'bottoms'],
            'optional': ['shoes', 'outerwear', 'accessories'],
            'style_notes': 'Perfect for everyday comfort and style'
        },
        'work': {
            'required': ['tops', 'bottoms'],
            'optional': ['shoes', 'outerwear', 'formal'],
            'style_notes': 'Professional and polished for the workplace'
        },
        'date': {
            'required': ['tops', 'bottoms'],
            'optional': ['shoes', 'accessories', 'dresses'],
            'style_notes': 'Stylish and romantic for special occasions'
        },
        'party': {
            'required': ['tops', 'bottoms'],
            'optional': ['shoes', 'accessories', 'dresses', 'formal'],
            'style_notes': 'Eye-catching and fun for celebrations'
        },
        'formal': {
            'required': ['formal', 'shoes'],
            'optional': ['accessories', 'outerwear'],
            'style_notes': 'Elegant and sophisticated for formal events'
        },
        'workout': {
            'required': ['activewear'],
            'optional': ['shoes'],
            'style_notes': 'Comfortable and functional for exercise'
        }
    }
    
    # Get rules for the occasion
    rules = outfit_rules.get(occasion, outfit_rules['casual'])
    
    # Create outfit names based on occasion and style
    outfit_names = {
        'casual': ['Relaxed Weekend Look', 'Everyday Comfort', 'Casual Chic'],
        'work': ['Professional Power', 'Office Ready', 'Business Casual'],
        'date': ['Date Night Glam', 'Romantic Evening', 'Special Occasion'],
        'party': ['Party Perfect', 'Night Out Style', 'Celebration Ready'],
        'formal': ['Formal Elegance', 'Black Tie Ready', 'Sophisticated Style'],
        'workout': ['Gym Ready', 'Active Lifestyle', 'Fitness Fashion']
    }
    
    names = outfit_names.get(occasion, ['Stylish Look', 'Fashion Forward', 'Perfect Combo'])
    
    # Try to create 3 different combinations
    for i in range(3):
        outfit_items = []
        used_items = set()
        
        # First, try to get required categories
        for req_category in rules['required']:
            if req_category in categories:
                available_items = [item for item in categories[req_category] if item.id not in used_items]
                if available_items:
                    # Prefer items that haven't been worn much
                    item = min(available_items, key=lambda x: x.times_worn)
                    outfit_items.append(item)
                    used_items.add(item.id)
        
        # Then add optional categories
        for opt_category in rules['optional']:
            if opt_category in categories and len(outfit_items) < 4:
                available_items = [item for item in categories[opt_category] if item.id not in used_items]
                if available_items:
                    # For variety, use different selection methods
                    if i == 0:  # First outfit: least worn
                        item = min(available_items, key=lambda x: x.times_worn)
                    elif i == 1:  # Second outfit: favorites
                        favorites = [item for item in available_items if item.favorite]
                        item = random.choice(favorites) if favorites else random.choice(available_items)
                    else:  # Third outfit: random
                        item = random.choice(available_items)
                    
                    outfit_items.append(item)
                    used_items.add(item.id)
        
        # Only create outfit if we have at least 2 items
        if len(outfit_items) >= 2:
            suggestions.append({
                'name': names[i] if i < len(names) else f'Outfit {i+1}',
                'description': f'A {style_preference} {occasion} outfit perfect for {season} weather',
                'style_notes': rules['style_notes'],
                'items': outfit_items,
                'item_ids': [item.id for item in outfit_items],
            })
    
    # If we couldn't create enough outfits, create simple random combinations
    while len(suggestions) < 3 and len(user_items) >= 2:
        outfit_items = random.sample(list(user_items), min(3, len(user_items)))
        suggestions.append({
            'name': f'Mix & Match {len(suggestions) + 1}',
            'description': f'A creative combination for {occasion}',
            'style_notes': 'Sometimes the best outfits come from unexpected combinations!',
            'items': outfit_items,
            'item_ids': [item.id for item in outfit_items],
        })
    
    return suggestions[:3]  # Return maximum 3 suggestions

@require_POST
def save_ai_outfit(request):
    """Save an AI-generated outfit to user's collection"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'})
    
    try:
        outfit_name = request.POST.get('outfit_name')
        outfit_description = request.POST.get('outfit_description')
        item_ids = request.POST.getlist('item_ids')
        occasion = request.POST.get('occasion', '')
        season = request.POST.get('season', 'all_season')
        
        # Create the outfit
        outfit = Outfit.objects.create(
            user=request.user,
            name=outfit_name,
            description=outfit_description,
            occasion=occasion,
            season=season
        )
        
        # Add items to the outfit
        items = WardrobeItem.objects.filter(id__in=item_ids, user=request.user)
        outfit.items.set(items)
        
        # Update stats
        stats, created = WardrobeStats.objects.get_or_create(user=request.user)
        stats.update_stats()
        
        messages.success(request, f'Outfit "{outfit_name}" has been saved to your collection!')
        return JsonResponse({'success': True, 'outfit_id': outfit.id})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def add_purchase_to_wardrobe(user, product, variations=None, purchase_price=None):
    """
    Utility function to automatically add purchased items to wardrobe
    This should be called from the order completion process
    """
    try:
        # Check if item already exists
        existing_item = WardrobeItem.objects.filter(
            user=user,
            store_product=product
        ).first()
        
        if existing_item:
            return existing_item
        
        # Create new wardrobe item
        item = WardrobeItem.objects.create(
            user=user,
            name=product.product_name,
            description=product.description,
            category='other',  # You might want to map product categories
            brand=getattr(product, 'brand', ''),
            image=product.images,
            source='store_purchase',
            store_product=product,
            purchase_price=purchase_price or product.price,
        )
        
        # Add variation information if available
        if variations:
            colors = [v.variation_value for v in variations if v.variation_category.lower() == 'color']
            sizes = [v.variation_value for v in variations if v.variation_category.lower() == 'size']
            
            if colors:
                item.color = colors[0]
            if sizes:
                item.size = sizes[0]
            
            item.save()
        
        # Update user stats
        stats, created = WardrobeStats.objects.get_or_create(user=user)
        stats.update_stats()
        
        return item
        
    except Exception as e:
        print(f"Error adding item to wardrobe: {e}")
        return None