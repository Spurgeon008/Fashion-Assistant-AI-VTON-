from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import WeatherData, DressRecommendation, WeatherOutfitRule
from store.models import Product
import random
import json
from datetime import datetime

def dress_recommender_home(request):
    """Main dress recommender page"""
    # Get or create dummy weather data
    weather_data = get_current_weather()
    
    # Get recent recommendations
    recent_recommendations = DressRecommendation.objects.all()[:3]
    
    context = {
        'weather_data': weather_data,
        'recent_recommendations': recent_recommendations,
    }
    
    return render(request, 'dress_recommender/home.html', context)

def get_weather_recommendation(request):
    """Get dress recommendation based on current weather"""
    if request.method == 'POST':
        city = request.POST.get('city', 'New York')
        
        # Get weather data (dummy for now)
        weather_data = get_current_weather(city)
        
        # Generate recommendation
        recommendation = generate_dress_recommendation(weather_data, request.user if request.user.is_authenticated else None)
        
        context = {
            'weather_data': weather_data,
            'recommendation': recommendation,
            'city': city,
        }
        
        return render(request, 'dress_recommender/recommendation.html', context)
    
    return redirect('dress_recommender:home')

def get_current_weather(city='New York'):
    """Get current weather data (dummy implementation)"""
    # Dummy weather data - in real implementation, this would call a weather API
    dummy_weather_conditions = [
        {
            'city': city,
            'temperature': random.uniform(-5, 35),
            'condition': random.choice(['sunny', 'cloudy', 'rainy', 'snowy', 'windy']),
            'humidity': random.randint(30, 90),
            'wind_speed': random.uniform(5, 25),
        }
    ]
    
    weather_info = random.choice(dummy_weather_conditions)
    weather_info['feels_like'] = weather_info['temperature'] + random.uniform(-3, 3)
    
    # Create or get weather data
    weather_data, created = WeatherData.objects.get_or_create(
        city=weather_info['city'],
        defaults=weather_info
    )
    
    # Update with latest data if not created
    if not created:
        for key, value in weather_info.items():
            setattr(weather_data, key, value)
        weather_data.save()
    
    return weather_data

def generate_dress_recommendation(weather_data, user=None):
    """Generate dress recommendation based on weather"""
    
    # Determine temperature range
    temp = weather_data.temperature
    if temp < 0:
        temp_range = 'very_cold'
    elif temp < 10:
        temp_range = 'cold'
    elif temp < 20:
        temp_range = 'cool'
    elif temp < 25:
        temp_range = 'mild'
    elif temp < 30:
        temp_range = 'warm'
    else:
        temp_range = 'hot'
    
    # Get recommendation rules
    recommendation_rules = get_weather_outfit_rules(weather_data.condition, temp_range)
    
    # Generate AI-like recommendation text
    recommendation_text = generate_recommendation_text(weather_data, temp_range)
    
    # Get suitable products
    suitable_products = get_suitable_products(weather_data.condition, temp_range)
    
    # Create recommendation object
    recommendation = DressRecommendation.objects.create(
        user=user,
        weather_data=weather_data,
        recommendation_text=recommendation_text,
        style_tips=recommendation_rules.get('style_advice', ''),
        color_suggestions=recommendation_rules.get('recommended_colors', ''),
        fabric_suggestions=recommendation_rules.get('recommended_fabrics', ''),
    )
    
    # Add suitable products
    if suitable_products:
        recommendation.recommended_products.set(suitable_products)
    
    return recommendation

def get_weather_outfit_rules(condition, temp_range):
    """Get outfit rules based on weather condition and temperature"""
    
    # Dummy rules - in real implementation, these could be stored in database
    rules = {
        ('sunny', 'hot'): {
            'recommended_categories': 'tops,bottoms,dresses',
            'recommended_colors': 'light colors,white,pastels,bright colors',
            'recommended_fabrics': 'cotton,linen,breathable fabrics',
            'style_advice': 'Choose light, breathable fabrics and bright colors. Avoid dark colors that absorb heat. Consider sun protection with hats and sunglasses.'
        },
        ('sunny', 'warm'): {
            'recommended_categories': 'tops,bottoms,dresses,casual',
            'recommended_colors': 'light colors,bright colors,summer tones',
            'recommended_fabrics': 'cotton,linen,light fabrics',
            'style_advice': 'Perfect weather for light, comfortable clothing. Mix and match bright colors and breathable fabrics.'
        },
        ('rainy', 'cool'): {
            'recommended_categories': 'outerwear,tops,bottoms,shoes',
            'recommended_colors': 'darker colors,navy,black,waterproof materials',
            'recommended_fabrics': 'waterproof,synthetic,quick-dry',
            'style_advice': 'Layer up with waterproof outer layers. Choose darker colors that won\'t show water stains. Don\'t forget waterproof shoes!'
        },
        ('cold', 'very_cold'): {
            'recommended_categories': 'outerwear,formal,tops,bottoms',
            'recommended_colors': 'dark colors,warm tones,layering colors',
            'recommended_fabrics': 'wool,fleece,insulated materials',
            'style_advice': 'Layer multiple pieces for warmth. Choose insulated fabrics and don\'t forget accessories like scarves and gloves.'
        },
        ('cloudy', 'mild'): {
            'recommended_categories': 'tops,bottoms,casual,outerwear',
            'recommended_colors': 'versatile colors,neutrals,earth tones',
            'recommended_fabrics': 'cotton,blends,comfortable materials',
            'style_advice': 'Great weather for versatile outfits. You can layer or go light depending on your comfort.'
        }
    }
    
    # Get the most specific rule or default
    rule_key = (condition, temp_range)
    if rule_key in rules:
        return rules[rule_key]
    
    # Fallback rules
    return {
        'recommended_categories': 'tops,bottoms,casual',
        'recommended_colors': 'versatile colors,neutrals',
        'recommended_fabrics': 'comfortable materials',
        'style_advice': 'Choose comfortable, weather-appropriate clothing that makes you feel confident.'
    }

def generate_recommendation_text(weather_data, temp_range):
    """Generate AI-like recommendation text"""
    
    condition = weather_data.condition
    temp = weather_data.temperature
    feels_like = weather_data.feels_like
    
    # Temperature-based recommendations
    temp_advice = {
        'very_cold': f"It's freezing at {temp:.1f}°C! Bundle up in warm layers, thick coats, and don't forget your winter accessories.",
        'cold': f"Chilly at {temp:.1f}°C. Perfect for cozy sweaters, warm jackets, and comfortable boots.",
        'cool': f"Cool and comfortable at {temp:.1f}°C. Great weather for light layers and transitional pieces.",
        'mild': f"Pleasant {temp:.1f}°C weather! You have lots of flexibility - go with what feels comfortable.",
        'warm': f"Lovely {temp:.1f}°C weather. Perfect for light, breathable fabrics and comfortable styles.",
        'hot': f"It's hot at {temp:.1f}°C! Stay cool with light colors, breathable fabrics, and minimal layers."
    }
    
    # Condition-based recommendations
    condition_advice = {
        'sunny': "The sun is shining! Consider sun protection and light colors that won't absorb too much heat.",
        'cloudy': "Overcast skies provide natural shade. Great day for versatile outfits.",
        'rainy': "Rain is expected! Waterproof layers and darker colors are your best friends today.",
        'snowy': "Snow is falling! Time for your warmest, most weather-resistant pieces.",
        'windy': "It's windy out there! Secure layers and avoid loose, flowing pieces that might be troublesome."
    }
    
    base_text = temp_advice.get(temp_range, f"The temperature is {temp:.1f}°C.")
    weather_text = condition_advice.get(condition, "Check the weather conditions before heading out.")
    
    feels_like_text = ""
    if abs(feels_like - temp) > 2:
        feels_like_text = f" It feels like {feels_like:.1f}°C due to humidity and wind conditions."
    
    return f"{base_text} {weather_text}{feels_like_text}"

def get_suitable_products(condition, temp_range):
    """Get products suitable for the weather condition"""
    
    # Define category mappings for different weather
    category_mappings = {
        'very_cold': ['outerwear', 'formal', 'activewear'],
        'cold': ['outerwear', 'tops', 'formal'],
        'cool': ['tops', 'outerwear', 'casual'],
        'mild': ['tops', 'bottoms', 'casual', 'dresses'],
        'warm': ['tops', 'bottoms', 'dresses', 'casual'],
        'hot': ['tops', 'dresses', 'casual'],
    }
    
    suitable_categories = category_mappings.get(temp_range, ['tops', 'bottoms', 'casual'])
    
    # Get products from suitable categories
    products = Product.objects.filter(
        category__category_name__icontains=suitable_categories[0],
        is_available=True
    )[:6]  # Limit to 6 products
    
    # If no products found, get any available products
    if not products.exists():
        products = Product.objects.filter(is_available=True)[:6]
    
    return products

@require_POST
def save_recommendation(request):
    """Save a recommendation to user's favorites"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'})
    
    try:
        recommendation_id = request.POST.get('recommendation_id')
        recommendation = DressRecommendation.objects.get(id=recommendation_id)
        
        # Update the recommendation to be associated with the user
        recommendation.user = request.user
        recommendation.save()
        
        messages.success(request, 'Recommendation saved to your profile!')
        return JsonResponse({'success': True})
        
    except DressRecommendation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Recommendation not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def my_recommendations(request):
    """View user's saved recommendations"""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please sign in to view your saved recommendations.')
        return redirect('accounts:login')
    
    recommendations = DressRecommendation.objects.filter(user=request.user)
    
    context = {
        'recommendations': recommendations,
    }
    
    return render(request, 'dress_recommender/my_recommendations.html', context)