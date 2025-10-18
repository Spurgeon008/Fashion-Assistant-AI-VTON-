"""
Weather-based clothing recommendations
"""
import requests
from django.conf import settings

def get_weather(city='London'):
    """
    Get current weather for a city using OpenWeatherMap API
    Returns: dict with temperature, condition, etc.
    """
    api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
    
    if not api_key:
        # Return default weather if no API key
        return {
            'temp': 20,
            'condition': 'Clear',
            'description': 'clear sky',
            'icon': '01d'
        }
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'temp': data['main']['temp'],
                'condition': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
    except Exception as e:
        print(f"Weather API error: {e}")
    
    # Return default if API fails
    return {
        'temp': 20,
        'condition': 'Clear',
        'description': 'clear sky',
        'icon': '01d'
    }

def get_clothing_recommendations(weather_data):
    """
    Recommend clothing categories based on weather
    """
    temp = weather_data['temp']
    condition = weather_data['condition'].lower()
    
    recommendations = {
        'categories': [],
        'message': '',
        'style_tips': []
    }
    
    # Temperature-based recommendations
    if temp < 10:
        recommendations['categories'] = ['jacket', 'coat', 'sweater', 'boots']
        recommendations['message'] = f"It's cold ({temp}°C)! Stay warm with these items:"
        recommendations['style_tips'] = [
            'Layer up with warm clothing',
            'Don\'t forget a scarf and gloves',
            'Wear insulated boots'
        ]
    elif temp < 20:
        recommendations['categories'] = ['jacket', 'jeans', 'shirt', 'sneakers']
        recommendations['message'] = f"Mild weather ({temp}°C). Perfect for:"
        recommendations['style_tips'] = [
            'Light jacket recommended',
            'Comfortable casual wear',
            'Closed-toe shoes'
        ]
    elif temp < 30:
        recommendations['categories'] = ['t-shirt', 'shorts', 'dress', 'sandals']
        recommendations['message'] = f"Warm weather ({temp}°C)! Stay cool with:"
        recommendations['style_tips'] = [
            'Light, breathable fabrics',
            'Comfortable summer wear',
            'Sun protection recommended'
        ]
    else:
        recommendations['categories'] = ['tank-top', 'shorts', 'sandals', 'hat']
        recommendations['message'] = f"Hot weather ({temp}°C)! Beat the heat with:"
        recommendations['style_tips'] = [
            'Wear light colors',
            'Stay hydrated',
            'Protect from sun'
        ]
    
    # Weather condition adjustments
    if 'rain' in condition or 'drizzle' in condition:
        recommendations['categories'].append('raincoat')
        recommendations['style_tips'].append('Bring an umbrella or raincoat')
    
    if 'snow' in condition:
        recommendations['categories'] = ['coat', 'boots', 'sweater', 'scarf']
        recommendations['message'] = f"Snowy weather! Bundle up:"
        recommendations['style_tips'] = ['Waterproof boots essential', 'Multiple layers recommended']
    
    return recommendations
