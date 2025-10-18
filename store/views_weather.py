"""
Weather-based clothing recommendation views
"""
from django.shortcuts import render
from .weather import get_weather, get_clothing_recommendations
from .models import Product

def weather_recommendations(request):
    """Display weather-based clothing recommendations"""
    
    # Get city from request or use default
    city = request.GET.get('city', 'London')
    
    # Get weather data
    weather_data = get_weather(city)
    
    # Get recommendations
    recommendations = get_clothing_recommendations(weather_data)
    
    # Get products matching recommended categories
    recommended_products = []
    for category_name in recommendations['categories']:
        products = Product.objects.filter(
            product_name__icontains=category_name,
            is_available=True
        )[:4]  # Limit to 4 products per category
        if products:
            recommended_products.extend(products)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_products = []
    for product in recommended_products:
        if product.id not in seen:
            seen.add(product.id)
            unique_products.append(product)
    
    context = {
        'weather': weather_data,
        'recommendations': recommendations,
        'products': unique_products[:12],  # Limit to 12 products total
        'city': city,
    }
    
    return render(request, 'store/weather_recommendations.html', context)
